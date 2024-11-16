from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",env_file_encoding="utf-8",extra="ignore")

    api_prefix: str
    debug:bool
    project_name: str
    version: str
    description: str
    static_dir: str

    host: str
    port: int
    
    google_cloud_api_key: str = Field(...,description="Google Cloud API Key",validate_default=True)

