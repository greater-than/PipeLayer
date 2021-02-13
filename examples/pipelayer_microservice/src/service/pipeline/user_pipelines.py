# region imports
from pipelayer import FilterEventArgs, Pipeline, Switch
from pipelayer.protocol import IFilter

from service.mapper import map_resreq, map_user
from service.mapper.map_request import (MapFindUserRequest, MapUserRequest,
                                        MapUsersRequest)
from service.model.not_found_model import NotFound
from service.provider.user import IUserProvider
from service.provider.user.resreq import ResReqUserProvider

# endregion


map_users_pipeline: Pipeline = Pipeline(
    name="Map Users Pipeline",
    steps=[
        map_resreq.from_resreq_list_api_response,
        map_user.from_resreq_list
    ])


def get_user_pipeline(user_provider: IUserProvider = ResReqUserProvider) -> Pipeline:

    map_user_request = MapUserRequest("Map User")

    return Pipeline(
        name="Get User Pipeline",
        steps=[
            map_user_request,
            # ↓ output is piped to next step
            user_provider.get_user,
            # ↓
            map_resreq.from_resreq_api_response,
            # ↓
            map_user.from_resreq_model
        ])


def get_users_pipeline(user_provider: IUserProvider = ResReqUserProvider) -> Pipeline:

    def map_users_request_end(sender: IFilter, args: FilterEventArgs):
        if args.data:
            print("end event handled")

    map_users_request = MapUsersRequest("Map User")
    map_users_request.end.append(map_users_request_end)

    return Pipeline(
        name="Get Users Pipeline",
        steps=[
            map_users_request,
            user_provider.get_users,
            map_users_pipeline,
            Switch(
                lambda d, c: bool(d.__root__),
                {
                    True:
                        lambda d, c: d,
                    False: lambda d, c:
                        NotFound(message="No users found")
                }
            )
        ])


def find_users_pipeline(user_provider: IUserProvider) -> Pipeline:

    map_request = MapFindUserRequest("Map User")

    return Pipeline(
        name="Find Users Pipeline",
        steps=[
            map_request,
            user_provider.find_users,
            map_resreq.from_resreq_list_api_response,
            map_users_pipeline
        ]
    )
