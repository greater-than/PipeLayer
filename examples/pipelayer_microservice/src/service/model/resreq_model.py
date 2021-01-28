from typing import List, Optional

from pydantic import BaseModel


class Support(BaseModel):
    url: Optional[str]
    text: Optional[str]


class ResReqBase(BaseModel):
    support: Support


class ResReqModel(ResReqBase):
    data: dict


class ResReqList(ResReqBase):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: List[dict]
