class Config:
    client_id: str = "third-party-app"
    client_secret: str = ""
    scope: str = "solver-director:projects:read"
    server_metadata_url: str = (
        "http://local/api/user/v1/.well-known/openid-configuration"
    )
