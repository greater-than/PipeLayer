from typing import Optional

from pydantic import BaseModel


class BaseRequest(BaseModel):
    api_name: str


class ListRequest(BaseRequest):
    page: Optional[int] = 1
    per_page: Optional[int] = 6


class UserRequest(BaseRequest):
    id: Optional[int]
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    avatar: Optional[str]
    api_name: str = "users"


class UserListRequest(ListRequest):
    api_name: str = "users"


class UserSearchRequest(UserListRequest, UserRequest):
    search_all: Optional[bool] = True
