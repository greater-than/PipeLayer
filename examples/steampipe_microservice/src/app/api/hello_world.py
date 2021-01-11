from logging import Logger

from app.api import handle_exception
from app.config.app_context import AppContext
from app.config.app_settings import AppSettings
from app.step.hello_world import HelloWorld
from steampipe.pipeline import Pipeline


def hello_world():
    context = AppContext(AppSettings, Logger())
    pipeline = Pipeline.create(name="Hello World", context=context)
    steps = [HelloWorld(
        name="Hello World Step",
        post_process=HelloWorld.PostProcess.create_response
    )]

    try:
        return pipeline.run(steps=steps, data="Bonjour le monde")

    except Exception as e:
        return handle_exception(e)
