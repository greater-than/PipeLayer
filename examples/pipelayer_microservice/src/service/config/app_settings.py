from __future__ import annotations

from pydantic import BaseModel


class AppSettings(BaseModel):
    user_service_api: str
