from abc import ABC, abstractmethod

from service.config.app_context import AppContext
from service.model.request_model import (UserListRequest, UserRequest,
                                         UserSearchRequest)


class IUserProvider(ABC):

    @abstractmethod
    def get_user(self, request: UserRequest, context: AppContext) -> dict:
        pass

    @abstractmethod
    def get_users(self, request: UserListRequest, context: AppContext) -> dict:
        pass

    @abstractmethod
    def find_users(self, request: UserSearchRequest, context: AppContext) -> dict:
        pass
