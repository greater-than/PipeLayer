from typing import Callable, Union

from pipelayer import Pipeline, Step
from service.filter.mapper.map_request_filter import MapRequest
from service.filter.mapper.map_resreq_filter import MapResReq
from service.filter.mapper.map_user_filter import MapUser
from service.filter.resreq_filter import ResReq

get_user_pipeline: Pipeline = Pipeline(
    name="Get User Pipeline",
    steps=[
        ResReq.get_user,
        MapResReq.from_single_response,
        MapUser.from_resreq_single_response
    ]
)


def users_pipeline(get_users_step: Union[Step, Callable]) -> Pipeline:
    return Pipeline(
        name="Get Users Pipeline",
        steps=[
            MapRequest.from_users_request,
            get_users_step,
            MapResReq.from_list_response,
            MapUser.from_resreq_list_response
        ]
    )


get_paged_users_pipeline: Pipeline = users_pipeline(ResReq.get_paged_users)

get_all_users_pipeline: Pipeline = users_pipeline(ResReq.get_users)

find_users_pipeline: Pipeline = users_pipeline(ResReq.find_users)
