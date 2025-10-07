import asyncio
import requests
from authlib.integrations.requests_client import OAuth2Session
from .config import Config


def main():
    endpoints = get_endpoints()

    session = OAuth2Session(
        client_id=Config.client_id,
        client_secret=Config.client_secret,
        scope=Config.scope,
        token_endpoint=endpoints["token_endpoint"],
    )

    with session:
        get_token(session)
        user_test(session)


def get_token(session: OAuth2Session):
    return session.fetch_token(username="admin", password="admin")


def user_test(session: OAuth2Session):
    response = session.get("http://local/api/user/v1/test")
    response.raise_for_status()
    print(response.json())


def get_endpoints() -> dict:
    return requests.get(Config.server_metadata_url).json()


if __name__ == "__main__":
    main()
