from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Configuration settings for the ToDo application.

    Attributes:
        app_name (str): name of the application 
        debug (bool): variable to enable or disable debug mode 
    """
    app_name: str = "ToDo App"
    debug: bool = False

    class Config:
        """
        Configuration for loading environment variables.

        Attributes:
            env_file (str): name of the environment file
        """
        env_file: str = ".env"