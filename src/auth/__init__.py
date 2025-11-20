import requests
from config import Config
from joserfc import jwt
from joserfc.jwt import Token
from joserfc.jwk import KeySet


class Auth:
    config: Config

    def __init__(self, config: Config):
        self.config = config

    def discover_endpoints(self) -> dict:
        r = requests.get(
            self.config.server_metadata_url, timeout=self.config.Timeout.default
        )
        r.raise_for_status()
        return r.json()

    def jwks_url(self) -> str:
        return self.discover_endpoints()["jwks_uri"]

    def jwt_keys(self) -> dict:
        r = requests.get(self.jwks_url(), timeout=self.config.Timeout.default)
        r.raise_for_status()
        return r.json()

    def decode_token(self, token: str) -> Token:
        key_set = KeySet.import_key_set(self.jwt_keys())
        return jwt.decode(token, key_set)
