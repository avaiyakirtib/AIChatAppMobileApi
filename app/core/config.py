from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    # Load settings from the .env file
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8"
    )

    TRUSTED_ADMIN_API_KEY: str
    
    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str

    # JWT Settings
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    # Google SSO
    # Step 1: Read the environment variable as a plain string to avoid parsing errors.
    GOOGLE_CLIENT_IDS_STR: str

    # Apple SSO
    APPLE_BUNDLE_ID: str
    
    # Step 2: Create a property that splits the string into a list for the app to use.
    @property
    def GOOGLE_CLIENT_IDS(self) -> List[str]:
        """
        Parses the comma-separated string of Google Client IDs into a list.
        """
        return [item.strip() for item in self.GOOGLE_CLIENT_IDS_STR.split(',')]


# Create a single instance of the settings to be used in the app
settings = Settings()