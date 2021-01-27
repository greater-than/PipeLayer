import json

import requests

from service.config import AppContext
from service.model.request_model import ListRequest, UsersRequest
from service.model.resreq_model import ResReqSingleResponse


class ResReq:

    @staticmethod
    def get_user(id: int, context: AppContext) -> ResReqSingleResponse:
        req = f"{context.settings.resreq_api}/users/{id}"
        resreq_resp = requests.get(req)
        resp = json.loads(resreq_resp.content)
        context.log.info("User received from ResReq")
        return resp

    @staticmethod
    def get_paged_users(request: ListRequest, context: AppContext) -> dict:
        req = f"{context.settings.resreq_api}/users?page={request.page}&per_page={request.per_page}"
        resreq_resp = requests.get(req)
        resp = json.loads(resreq_resp.content)
        context.log.info("Users received from ResReq")
        return resp

    @staticmethod
    def get_users(request: UsersRequest, context: AppContext) -> dict:
        page = request.page
        resp = {}
        while page <= request.max_pages:
            req = f"{context.settings.resreq_api}/users?page={page}&per_page={request.per_page}"
            resreq_resp = requests.get(req)
            content = json.loads(resreq_resp.content)
            page += 1
            if not resp:
                resp = content
            else:
                resp["page"] = page
                resp["data"].append(content["data"])

        context.log.info("Users received from ResReq")
        return resp

    @staticmethod
    def find_users(request: UsersRequest, context: AppContext) -> dict:
        users = ResReq.get_users(request, context)
        users["data"] = [
            user for user in users["data"]
            if request.email in user["email"] and
            request.first_name in user["first_name"] and
            request.last_name in user["last_name"] and
            request["avatar"] in user["avatar"]
        ]
