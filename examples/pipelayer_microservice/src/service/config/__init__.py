from logging import Logger

from service.config.app_context import AppContext
from service.config.app_settings import AppSettings

context = AppContext(AppSettings(), Logger("Service Logger"))
