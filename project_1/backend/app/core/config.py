from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ExamRAG"
    app_version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"
    debug: bool = False
    database_url: str = "sqlite:///./examrag.db"
    database_echo: bool = False
    secret_key: str = "examrag-local-development-secret-key-please-change"
    frontend_url: str = "http://localhost:8080"
    cors_origins: str = "http://localhost:8080,http://127.0.0.1:8080,http://localhost:3000,https://*.vercel.app"
    openai_api_key: str = ""
    embedding_api_key: str = ""
    resend_api_key: str = ""
    resend_from_email: str = "no-reply@example.com"
    app_base_url: str = "http://localhost:8000"
    admin_email: str = "admin@example.com"
    admin_password: str = "Admin123!"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def api_prefix(self) -> str:
        return self.api_v1_prefix


settings = Settings()
