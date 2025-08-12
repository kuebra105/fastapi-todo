from fastapi import APIRouter, Depends
from typing import Annotated
from app.dependencies.config import Settings

router = APIRouter()

settings_instance = Settings()

SettingsDep = Annotated[Settings, Depends(lambda: settings_instance)]

@router.get("/info")
def get_info(settings: SettingsDep):
    return {
        "app_name": settings.app_name,
        "debug": settings.debug
    }