from pipelayer import Filter
from pipelayer.filter import raise_events

from service.config.app_context import AppContext
from service.model.request_model import (UserListRequest, UserRequest,
                                         UserSearchRequest)


class MapUserRequest(Filter):
    def run(self, request: dict, context: AppContext) -> UserRequest:
        return UserRequest(**request)


class MapUsersRequest(Filter):

    @raise_events
    def run(self, request: dict, context: AppContext) -> UserListRequest:
        return UserListRequest(**request)


class MapFindUserRequest(Filter):
    def run(self, request: dict, context: AppContext) -> UserSearchRequest:
        return UserSearchRequest(**request)
