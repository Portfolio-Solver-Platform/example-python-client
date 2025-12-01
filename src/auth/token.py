from auth.core import Auth
from typing import Callable
import logging
import requests
import time

logger = logging.getLogger(__name__)


class Token:
    _auth: Auth
    _access_token: str
    _refresh_token: str | None
    _auth_func: Callable[[], tuple[str, str | None, int | None]]
    _refresh_timeout: tuple[int, int]
    _leeway: int
    _access_token_expires_at: int

    def __init__(
        self,
        auth: Auth,
        auth_func: Callable[[], tuple[str, str | None, int | None]],
        lazy: bool = False,
        refresh_timeout: tuple[int, int] = (1, 5),
        leeway: int = 15,
    ):
        self._refresh_timeout = refresh_timeout
        self._auth_func = auth_func
        self._auth = auth
        self._leeway = leeway

        if not lazy:
            self.authenticate()

    def get(self) -> str:
        if self.is_expired():
            self.refresh()

        return self._access_token

    def _set_token(
        self,
        access_token: str,
        refresh_token: str | None,
        refresh_expires_in: int | None,
    ) -> None:
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._update_expirations(refresh_expires_in)

    def _update_expirations(self, refresh_expires_in: int | None) -> None:
        self._access_token_expires_at = self.claims()["exp"]
        if refresh_expires_in is not None:
            self._refresh_token_expires_at = time.time() + refresh_expires_in

    def claims(self) -> dict:
        return self._auth.decode_token(self._access_token).claims

    def is_expired(self) -> bool:
        if self._access_token is None:
            return True

        return time.time() > (self._access_token_expires_at - self._leeway)

    def authenticate(self) -> None:
        access_token, refresh_token, refresh_expires_in = self._auth_func()
        self._set_token(access_token, refresh_token, refresh_expires_in)

    def refresh(self) -> None:
        if self._refresh_token is None:
            self.authenticate()

        if time.time() > (self._refresh_token_expires_at - self._leeway):
            self.authenticate()
            return

        endpoint = self._auth.endpoints()["token_endpoint"]

        data = self._auth.client_data() | {
            "grant_type": "refresh_token",
            "refresh_token": self._refresh_token,
        }
        r = requests.post(endpoint, data=data, timeout=self._refresh_timeout)
        r.raise_for_status()
        data = r.json()

        self._set_token(
            data["access_token"],
            data.get("refresh_token"),
            data.get("refresh_expires_in"),
        )
