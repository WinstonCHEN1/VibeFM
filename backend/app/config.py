from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    NETEASE_API: str = "http://netease-api:3000"
    REDIS_URL: str = "redis://redis:6379/0"
    DATABASE_URL: str = "sqlite:////data/fm.db"
    INVITE_CODES: str = "letmein"
    NETEASE_COOKIE: str = ""
    SECRET_KEY: str = "please-change-me"
    FALLBACK_PLAYLIST_ID: str = ""

    PER_USER_QUEUE_LIMIT: int = 10
    SAME_SONG_COOLDOWN_SEC: int = 1800
    PREFETCH_LEAD_SEC: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()


def invite_code_set() -> set[str]:
    return {c.strip() for c in settings.INVITE_CODES.split(",") if c.strip()}
