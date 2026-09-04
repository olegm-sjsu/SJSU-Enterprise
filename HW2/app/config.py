# Author: Oleg Mrynskyi
# CMPE 272 HW2 - GitHub Issues REST API & Webhook Service

import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

ENV_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))

class Settings(BaseSettings):
    # required env vars: GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPO, WEBHOOK_SECRET
    GITHUB_TOKEN: str = ""
    GITHUB_OWNER: str = ""
    GITHUB_REPO: str = ""
    WEBHOOK_SECRET: str = ""
    PORT: int = 8000
    DATABASE_PATH: str = "events.db"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    @field_validator("GITHUB_TOKEN", "GITHUB_OWNER", "GITHUB_REPO", "WEBHOOK_SECRET", mode="before")
    @classmethod
    def strip_comments_and_whitespace(cls, v: str) -> str:
        # people sometimes leave `# comment` trailing in .env files, strip that off
        if isinstance(v, str):
            v = v.split("#")[0].strip()
        return v

    def validate_settings(self) -> None:
        missing = []
        if not self.GITHUB_TOKEN:
            missing.append("GITHUB_TOKEN")
        if not self.GITHUB_OWNER:
            missing.append("GITHUB_OWNER")
        if not self.GITHUB_REPO:
            missing.append("GITHUB_REPO")
        if not self.WEBHOOK_SECRET:
            missing.append("WEBHOOK_SECRET")
            
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")


def get_settings() -> Settings:
    return Settings(
        _env_file=ENV_FILE_PATH if os.path.exists(ENV_FILE_PATH) else None
    )
