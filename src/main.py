from auth.device_auth import DeviceAuth
from config import Config


def main():
    token = DeviceAuth(Config).token()
    print("==== Access token ====")
    print(token.get())
    print("==== Decoded access token claims ====")
    print(token.claims())
    print()


if __name__ == "__main__":
    main()
