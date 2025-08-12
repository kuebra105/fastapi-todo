from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "ToDo App"
    debug: bool = False

    class Config:
        env_file: str = ".env"