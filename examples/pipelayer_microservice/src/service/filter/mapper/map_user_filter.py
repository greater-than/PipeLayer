from typing import List

from service.config import AppContext
from service.model.resreq_model import ResReqListResponse, ResReqSingleResponse
from service.model.user_model import User


class MapUser:

    @staticmethod
    def from_resreq_single_response(resp: ResReqSingleResponse, context: AppContext) -> User:
        user = User.parse_obj(resp.data)
        context.log.info("User parsed from ResReqSingleResponse.")
        return user

    @staticmethod
    def from_resreq_list_response(resp: ResReqListResponse, context: AppContext) -> List[User]:
        users = [User.parse_obj(data) for data in resp.data]
        context.log.info("Users parsed from ResReqListResponse.")
        return users
