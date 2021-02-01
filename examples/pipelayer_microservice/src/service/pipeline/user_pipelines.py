from pipelayer import Pipeline
from service.filter.mapper.map_request_filter import MapRequest
from service.filter.mapper.map_resreq_filter import MapResReq
from service.filter.mapper.map_user_filter import MapUser
from service.filter.resreq_filter import ResReq

get_user_pipeline: Pipeline = Pipeline(
    name="Get User Pipeline",
    steps=[
        MapRequest.from_get_user_request,
        ResReq.get_user,
        MapResReq.from_resreq_api_response,
        MapUser.from_resreq_model
    ]
)

get_users_pipeline: Pipeline = Pipeline(
    name="Get Users Pipeline",
    steps=[
        MapRequest.from_get_users_request,
        ResReq.get_users,
        MapResReq.from_resreq_list_api_response,
        MapUser.from_resreq_list
    ]
)

find_users_pipeline: Pipeline = Pipeline(
    name="Find Users Pipeline",
    steps=[
        MapRequest.from_find_user_request,
        ResReq.find_users,
        MapResReq.from_resreq_list_api_response,
        MapUser.from_resreq_list
    ]
)
