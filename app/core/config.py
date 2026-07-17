from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class UserSettings(BaseModel):
    default_scan_interval_minutes: int = 30
    default_max_nodes: int = 5
    default_notify_on_changes: bool = False


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_empty=True,
        env_nested_delimiter="__",
    )

    debug: bool = True
    database_dsn: str

    user_settings: UserSettings = UserSettings()


settings = Settings()


