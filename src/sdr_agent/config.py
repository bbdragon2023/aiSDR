"""Configuration management for SDR Agent."""

from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Anthropic API
    anthropic_api_key: str = Field(..., description="Anthropic API key for Claude")

    # Tavily API for research
    tavily_api_key: Optional[str] = Field(None, description="Tavily API key for web search")

    # SMTP Email Configuration
    smtp_host: str = Field("smtp.gmail.com", description="SMTP server host")
    smtp_port: int = Field(587, description="SMTP server port")
    smtp_username: Optional[str] = Field(None, description="SMTP username")
    smtp_password: Optional[str] = Field(None, description="SMTP password")
    smtp_from_email: Optional[str] = Field(None, description="From email address")
    smtp_from_name: str = Field("SDR Agent", description="From name")

    # Agent Configuration
    skills_dir: Path = Field(Path("./skills"), description="Directory containing skills")
    log_level: str = Field("INFO", description="Logging level")

    # Claude Model Configuration
    claude_model: str = Field("claude-sonnet-4-20250514", description="Claude model to use")
    max_tokens: int = Field(4096, description="Maximum tokens in response")

    @property
    def email_configured(self) -> bool:
        """Check if email is properly configured."""
        return all([self.smtp_username, self.smtp_password, self.smtp_from_email])


def get_settings() -> Settings:
    """Get application settings singleton."""
    return Settings()
