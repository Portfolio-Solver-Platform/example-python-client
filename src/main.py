from .device_auth import DeviceAuth
from .config import Config


def main():
    access_token, refresh_token = DeviceAuth(Config).get_token()
    print("==== Access token ====")
    print(access_token)
    print()
    print("==== Refresh token ====")
    print(refresh_token)


if __name__ == "__main__":
    main()
