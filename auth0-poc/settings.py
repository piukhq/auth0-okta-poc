from pydantic import BaseSettings


class Settings(BaseSettings):
    auth0_domain: str
    api_audience: str
    algorithms: list[str] = ["RS256"]
    session_key: str


settings = Settings()
