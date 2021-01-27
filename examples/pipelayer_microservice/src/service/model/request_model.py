from typing import Optional

from pydantic import BaseModel


class BaseRequest(BaseModel):
    ...


class ListRequest(BaseRequest):
    page: Optional[int] = 1
    per_page: Optional[int] = 6
    max_pages: Optional[int] = 2


class UserRequest(BaseRequest):
    id: Optional[int]
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    avatar: Optional[str]


class UsersRequest(UserRequest, ListRequest):
    ...
