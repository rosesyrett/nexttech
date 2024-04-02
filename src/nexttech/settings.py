from pydantic_settings import BaseSettings
from pydantic import Field

TABLE_NAME = "heimdall-features"
DYNAMODB_ENDPOINT_URL = "http://localhost:8080"

class Settings(BaseSettings):
    mongo_atlas_username: str = Field()
    mongo_atlas_password: str = Field()