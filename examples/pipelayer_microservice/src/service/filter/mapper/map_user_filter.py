from typing import List

from service.config import AppContext
from service.model.resreq_model import ResReqList, ResReqModel
from service.model.user_model import User, UserList


class MapUser:

    @staticmethod
    def from_resreq_model(resreq_model: ResReqModel, context: AppContext) -> User:
        user = User.parse_obj(resreq_model.data)
        context.log.info("User parsed from ResReqResponse.")
        return user

    @staticmethod
    def from_resreq_list(resreq_model: ResReqList, context: AppContext) -> List[User]:
        users = UserList.parse_obj(resreq_model.data)
        context.log.info("Users parsed from ResReqListResponse.")
        return users
