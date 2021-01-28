from typing import List

from service.config import AppContext
from service.model.resreq_model import ResReqList, ResReqModel
from service.model.user_model import User


class MapUser:

    @staticmethod
    def from_resreq_model(response: ResReqModel, context: AppContext) -> User:
        user = User.parse_obj(response.data)
        context.log.info("User parsed from ResReqResponse.")
        return user

    @staticmethod
    def from_resreq_list(response: ResReqList, context: AppContext) -> List[User]:
        users = [User.parse_obj(data) for data in response.data]
        context.log.info("Users parsed from ResReqListResponse.")
        return users
