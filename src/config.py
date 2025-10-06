class Config:
    client_id: str = "users"
    client_secret: str = ""
    scope: str = "profile email"
    server_metadata_url: str = (
        "http://local/api/user/v1/.well-known/openid-configuration"
    )
