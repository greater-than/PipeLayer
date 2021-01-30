from app.app_context import AppContext


def create_response(data: str, context: AppContext) -> dict:
    return {"message": data}
