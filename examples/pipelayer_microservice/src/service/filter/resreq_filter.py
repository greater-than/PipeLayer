import json

import requests

from service.config import AppContext
from service.model.request_model import (ListRequest, UserListRequest,
                                         UserRequest, UserSearchRequest)


class ResReq:

    @staticmethod
    def get_user(request: UserRequest, context: AppContext) -> dict:
        req = f"{context.settings.resreq_api}/{request.api_name}/{request.id}"
        resreq_resp = requests.get(req)
        user = json.loads(resreq_resp.content)
        context.log.info("User received from ResReq")
        return user

    @staticmethod
    def get_users(request: UserListRequest, context: AppContext) -> dict:
        users = ResReq.get_resreq_list(request, context)
        context.log.info("Users received from ResReq")
        return users

    @staticmethod
    def find_users(request: UserSearchRequest, context: AppContext) -> dict:
        users = ResReq.get_resreq_list(request, context)

        total = users["total"]
        items_remaining = total - (len(users["data"]) * request.per_page)

        if request.search_all and items_remaining > 0:
            remaining_items_request = ListRequest(page=request.page + 1, per_page=items_remaining)
            users["data"].append(ResReq.get_resreq_users(remaining_items_request, context)["data"])

        users["data"] = [
            user for user in users["data"]
            if request.email in user["email"] and
            request.first_name in user["first_name"] and
            request.last_name in user["last_name"] and
            request["avatar"] in user["avatar"]
        ]

        return users

    @staticmethod
    def get_resreq_list(request: ListRequest, context: AppContext) -> dict:
        req = f"{context.settings.resreq_api}/{request.api_name}?page={request.page}&per_page={request.per_page}"
        resreq_resp = requests.get(req)
        return json.loads(resreq_resp.content)
