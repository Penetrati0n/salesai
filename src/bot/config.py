"""Configuration management using pydantic settings."""

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow"
    )
    
    # Bot Configuration
    bot_token: str = Field(..., description="Telegram bot token")
    bot_username: Optional[str] = Field(None, description="Bot username")
    
    # Database Configuration
    database_url: str = Field(..., description="Database connection URL")
    database_test_url: Optional[str] = Field(None, description="Test database URL")
    
    # Redis Configuration
    redis_url: Optional[str] = Field(None, description="Redis connection URL")
    
    # Application Configuration
    debug: bool = Field(False, description="Debug mode")
    log_level: str = Field("INFO", description="Logging level")
    environment: str = Field("development", description="Environment")
    
    # Security
    secret_key: str = Field(..., description="Secret key for encryption")
    webhook_secret: Optional[str] = Field(None, description="Webhook secret")
    
    # External APIs
    openai_api_key: Optional[str] = Field(None, description="OpenAI API key")
    
    # Monitoring
    sentry_dsn: Optional[str] = Field(None, description="Sentry DSN")
    
    # Webhook Configuration
    webhook_url: Optional[str] = Field(None, description="Webhook URL")
    webhook_path: str = Field("/webhook", description="Webhook path")
    webhook_port: int = Field(8080, description="Webhook port")
    
    # Rate Limiting
    rate_limit_requests: int = Field(30, description="Rate limit requests per minute")
    rate_limit_window: int = Field(60, description="Rate limit window in seconds")
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment.lower() == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment.lower() == "production"


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()