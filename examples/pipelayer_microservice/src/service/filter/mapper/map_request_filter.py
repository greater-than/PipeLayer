from service.model.request_model import UserRequest, UsersRequest


class MapRequest:

    @staticmethod
    def from_users_request(request: dict) -> UsersRequest:
        return UsersRequest(**request)

    @staticmethod
    def from_user_request(request: dict) -> UserRequest:
        return UserRequest(**request)
