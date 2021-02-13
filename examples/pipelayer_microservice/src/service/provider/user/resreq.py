import json

import requests

from service.config import IAppContext
from service.model.request_model import (ListRequest, UserListRequest,
                                         UserRequest, UserSearchRequest)
from service.provider.user import IUserProvider


class ResReqUserProvider(IUserProvider):

    def get_user(request: UserRequest, context: IAppContext) -> dict:
        req = f"{context.settings.user_service_api}/{request.api_name}/{request.id}"
        resreq_resp = requests.get(req)
        user = json.loads(resreq_resp.content)
        context.log.info("User received from ResReq")
        return user

    def get_users(request: UserListRequest, context: IAppContext) -> dict:
        users = ResReqUserProvider.get_resreq_list(request, context)
        context.log.info("Users received from ResReq")
        return users

    def find_users(request: UserSearchRequest, context: IAppContext) -> dict:
        users = ResReqUserProvider.get_resreq_list(request, context)

        total = users["total"]
        items_remaining = total - (len(users["data"]) * request.per_page)

        if request.search_all and items_remaining > 0:
            remaining_items_request = ListRequest(page=request.page + 1, per_page=items_remaining)
            users["data"].append(ResReqUserProvider.get_users(remaining_items_request, context)["data"])

        users["data"] = [
            user for user in users["data"]
            if request.email in user["email"] and
            request.first_name in user["first_name"] and
            request.last_name in user["last_name"] and
            request["avatar"] in user["avatar"]
        ]

        context.log.info("Users received from ResReq")
        return users

    def get_resreq_list(request: ListRequest, context: IAppContext) -> dict:
        req = f"{context.settings.user_service_api}/{request.api_name}?page={request.page}&per_page={request.per_page}"
        resreq_resp = requests.get(req)
        return json.loads(resreq_resp.content)
