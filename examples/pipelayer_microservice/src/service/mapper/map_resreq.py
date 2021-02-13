from service.config.app_context import AppContext
from service.model.resreq_model import ResReqList, ResReqModel


def from_resreq_api_response(response: dict, context: AppContext) -> ResReqModel:
    resreq = ResReqModel.parse_obj(response)
    return resreq


def from_resreq_list_api_response(response: dict, context: AppContext) -> ResReqList:
    resreq_list = ResReqList.parse_obj(response)
    return resreq_list
