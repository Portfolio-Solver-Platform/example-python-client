from device_auth import DeviceAuth
from config import Config
import requests
from pprint import pprint


def main():
    access_token, refresh_token = DeviceAuth(Config).get_token()
    print("==== Access token ====")
    print(access_token)
    print()
    print("==== Refresh token ====")
    print(refresh_token)

    # groups(access_token)
    projects(access_token)


def groups(token: str):
    response = requests.get(
        "http://local/api/solverdirector/v1/groups",
        headers={"Authorization": f"Bearer {token}"},
        timeout=Config.Timeout.default,
    )
    pprint(response)
    response.raise_for_status()
    pprint(response.json())


def projects(token: str):
    response = requests.get(
        "http://local/api/solverdirector/v1/projects",
        headers={"Authorization": f"Bearer {token}"},
        timeout=Config.Timeout.default,
    )
    pprint(response)
    response.raise_for_status()
    pprint(response.json())


if __name__ == "__main__":
    main()
