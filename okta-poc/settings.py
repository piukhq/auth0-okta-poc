from pydantic import BaseSettings


class Settings(BaseSettings):
    okta_domain: str
    okta_client_id: str
    api_audience: str
    algorithms: list[str] = ["RS256"]
    session_key: str


settings = Settings()
