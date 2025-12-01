import requests
from config import Config
from joserfc import jwt
from joserfc.jwt import Token as JWTToken
from joserfc.jwk import KeySet


class Auth:
    config: Config
    _endpoints: dict | None
    _jwt_keys: dict | None

    def __init__(self, config: Config):
        self.config = config
        self._endpoints = None
        self._jwt_keys = None

    def endpoints(self) -> dict:
        if self._endpoints is None:
            self._endpoints = self._discover_endpoints()

        return self._endpoints

    def _discover_endpoints(self) -> dict:
        r = requests.get(
            self.config.server_metadata_url, timeout=self.config.Timeout.default
        )
        r.raise_for_status()
        return r.json()

    def jwks_url(self) -> str:
        return self.endpoints()["jwks_uri"]

    def jwt_keys(self) -> dict:
        if self._jwt_keys is None:
            self._jwt_keys = self._get_jwt_keys()

        return self._jwt_keys

    def _get_jwt_keys(self) -> dict:
        r = requests.get(self.jwks_url(), timeout=self.config.Timeout.default)
        r.raise_for_status()
        return r.json()

    def decode_token(self, token: str) -> JWTToken:
        key_set = KeySet.import_key_set(self.jwt_keys())
        return jwt.decode(token, key_set)

    def client_data(self) -> dict:
        return {
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
        }
