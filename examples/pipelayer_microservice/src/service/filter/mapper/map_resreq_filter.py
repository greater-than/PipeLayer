from service.config.app_context import AppContext
from service.model.resreq_model import ResReqListResponse, ResReqSingleResponse


class MapResReq:

    @staticmethod
    def from_single_response(data: dict, context: AppContext) -> ResReqSingleResponse:
        resreq = ResReqSingleResponse.parse_obj(data)
        return resreq

    @staticmethod
    def from_list_response(data: dict, context: AppContext) -> ResReqListResponse:
        resreq_list = ResReqListResponse.parse_obj(data)
        return resreq_list
