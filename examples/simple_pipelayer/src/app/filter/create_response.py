from app.app_context import AppContext


def create_response(context: AppContext, data: str) -> dict:
    return {"message": data}
