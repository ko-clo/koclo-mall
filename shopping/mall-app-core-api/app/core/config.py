from urllib.parse import quote_plus, urlparse, urlunparse

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Application
    app_name: str = "Ko&Clo Mall API"
    debug: bool = False

    # Database
    database_url: str = "postgresql+asyncpg://mall:mall_dev_password@localhost:5432/mall_dev"

    @property
    def database_url_encoded(self) -> str:
        """URL-encoded database URL (특수문자 처리)."""
        parsed = urlparse(self.database_url)
        if parsed.password:
            encoded_password = quote_plus(parsed.password)
            netloc = f"{parsed.username}:{encoded_password}@{parsed.hostname}"
            if parsed.port:
                netloc += f":{parsed.port}"
            return urlunparse(parsed._replace(netloc=netloc))
        return self.database_url

    # CORS
    cors_origins: list[str] = ["http://localhost:5173"]

    # Supabase
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""
    supabase_jwt_secret: str = ""

    # Cloudflare R2
    r2_account_id: str = ""
    r2_access_key_id: str = ""
    r2_secret_access_key: str = ""
    r2_bucket_name: str = ""
    r2_public_url: str = ""


settings = Settings()
