from auth import Auth
from device_auth import DeviceAuth
from config import Config
import requests
from pprint import pprint


def main():
    auth = Auth(Config)
    access_token, refresh_token = DeviceAuth(Config).get_token()
    print("==== Access token ====")
    print(access_token)
    print("==== Decoded access token claims ====")
    print(auth.decode_token(access_token).claims)
    print()
    print("==== Refresh token ====")
    print(refresh_token)


if __name__ == "__main__":
    main()
