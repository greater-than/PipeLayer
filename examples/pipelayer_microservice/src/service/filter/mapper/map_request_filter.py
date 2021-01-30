from service.config.app_context import AppContext
from service.model.request_model import (UserListRequest, UserRequest,
                                         UserSearchRequest)


class MapRequest:

    @staticmethod
    def from_get_user_request(request: dict, context: AppContext) -> UserRequest:
        return UserRequest(**request)

    @staticmethod
    def from_get_users_request(request: dict, context: AppContext) -> UserListRequest:
        return UserListRequest(**request)

    @staticmethod
    def from_find_user_request(request: dict, context: AppContext) -> UserSearchRequest:
        return UserSearchRequest(**request)
