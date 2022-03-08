from pydantic import BaseSettings


class Settings(BaseSettings):
    auth0_domain: str
    auth0_mgmt_token: str
    api_audience: str
    algorithms: list[str] = ["RS256"]
    session_key: str


settings = Settings()
