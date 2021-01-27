from typing import List, Optional

from pydantic import BaseModel


class Support(BaseModel):
    url: Optional[str]
    text: Optional[str]


class ResReqBaseResponse(BaseModel):
    support: Support


class ResReqSingleResponse(ResReqBaseResponse):
    data: dict


class ResReqListResponse(ResReqBaseResponse):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: List[dict]
