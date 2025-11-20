from auth import Auth
from auth.device_auth import DeviceAuth
from config import Config


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
