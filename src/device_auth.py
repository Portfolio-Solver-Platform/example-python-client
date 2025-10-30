import time
import requests
from .config import Config


class DeviceAuth:
    config: Config

    def __init__(self, config: Config):
        self.config = config

    def discover_endpoints(self):
        r = requests.get(self.config.server_metadata_url)
        r.raise_for_status()
        return r.json()

    def request_device_code(self, device_endpoint):
        data = {"client_id": self.config.client_id, "scope": self.config.scope}
        r = requests.post(device_endpoint, data=data)
        r.raise_for_status()
        return r.json()

    def poll_token(self, token_endpoint, device_code, interval):
        while True:
            time.sleep(interval)
            data = {
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "device_code": device_code,
                "client_id": self.config.client_id,
            }
            r = requests.post(token_endpoint, data=data)
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 400:
                err = r.json().get("error")
                if err in ("authorization_pending", "slow_down"):
                    if err == "slow_down":
                        interval += 5
                    continue
                elif err == "expired_token":
                    raise RuntimeError("Device code expired.")
                else:
                    raise RuntimeError(f"Error: {err}")
            else:
                r.raise_for_status()

    def get_token(self) -> tuple[dict, dict | None]:
        """
        Initiatise the device authorization flow.
        When it is finished, it returns the access token and refresh token.
        """
        conf = self.discover_endpoints()
        device_auth_url = conf["device_authorization_endpoint"]
        token_url = conf["token_endpoint"]

        device_info = self.request_device_code(device_auth_url)
        print("Go to:", device_info["verification_uri"])
        print("Enter code:", device_info["user_code"])

        token_response = self.poll_token(
            token_url, device_info["device_code"], device_info.get("interval", 5)
        )

        return token_response["access_token"], token_response.get("refresh_token")
