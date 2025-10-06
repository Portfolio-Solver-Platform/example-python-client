import asyncio
import requests
from authlib.integrations.requests_client import OAuth2Session
from .config import Config


def main():
    endpoints = get_endpoints()

    client = OAuth2Session(
        client_id=Config.client_id,
        client_secret=Config.client_secret,
        scope=Config.scope,
        token_endpoint=endpoints["token_endpoint"],
    )

    token = client.fetch_token(username="admin", password="admin")
    print(token)


def get_endpoints() -> dict:
    return requests.get(Config.server_metadata_url).json()


if __name__ == "__main__":
    main()
