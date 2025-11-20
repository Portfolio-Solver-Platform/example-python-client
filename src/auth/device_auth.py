import time
import requests
import webbrowser
from config import Config


class DeviceAuth:
    config: Config

    def __init__(self, config: Config):
        self.config = config

    def get_token(self) -> tuple[dict, dict | None]:
        """
        Initiatise the device authorization flow.
        When it is finished, it returns the access token and refresh token.
        """
        conf = self._discover_endpoints()
        device_auth_url = conf["device_authorization_endpoint"]
        token_url = conf["token_endpoint"]

        device_info = self._request_device_code(device_auth_url)

        self._verify_user(device_info)
        token_response = self._poll_token(
            token_url, device_info["device_code"], device_info.get("interval", 5)
        )

        return token_response["access_token"], token_response.get("refresh_token")

    def _verify_user(self, device_info: dict):
        complete_uri = device_info.get("verification_uri_complete")
        if complete_uri:
            print("Opening login window in your browser...")
            webbrowser.open(complete_uri)
            print(
                "If it did not open, go to:", device_info["verification_uri_complete"]
            )
            print()
            print("Or alternatively,")

        print("Go to:", device_info["verification_uri"])
        print("And enter code:", device_info["user_code"])

    def _discover_endpoints(self):
        r = requests.get(
            self.config.server_metadata_url, timeout=self.config.Timeout.default
        )
        r.raise_for_status()
        return r.json()

    def _client_data(self):
        return {
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
        }

    def _request_device_code(self, device_endpoint):
        data = self._client_data() | {
            "scope": self.config.scope,
        }
        r = requests.post(
            device_endpoint, data=data, timeout=self.config.Timeout.default
        )
        r.raise_for_status()
        return r.json()

    def _poll_token(self, token_endpoint, device_code, interval):
        while True:
            time.sleep(interval)
            data = self._client_data() | {
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "device_code": device_code,
            }
            r = requests.post(
                token_endpoint, data=data, timeout=self.config.Timeout.default
            )
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
