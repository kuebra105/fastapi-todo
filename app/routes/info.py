from fastapi import APIRouter, Depends
from app.dependencies.config import Settings

router = APIRouter()

@router.get("/info")
def get_info(settings: Settings = Depends()):
    """
    Returns basic application information from the settings.

    Args:
        settings (Settings): injected settings dependency

    Returns:
        dict: dictionary containing the application name and debug status
    """
    return {"app_name": settings.app_name, "debug": settings.debug}