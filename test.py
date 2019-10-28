from middleware_manager.base import MiddlewareManagerBase
from middleware_manager import MiddlewareMixin
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class FirstMiddleware(MiddlewareMixin):

    def process_request(self, request=None):
        logger.info("Processing request FirstMiddleware {}".format(request))

    def process_response(self, request=None, response=None):
        logger.info("Processing response FirstMiddleware {}".format(request, response))


class SecondMiddleware(MiddlewareMixin):

    def process_request(self, request=None):
        logger.info("Processing response SecondMiddleware {}".format(request))


class ThirdMiddleware(MiddlewareMixin):

    def process_exception(self, request=None):
        logger.info("Processing exception ThirdMiddleware {}".format(request))


class FourthMiddleware(MiddlewareMixin):

    def process_exception(self, request=None):
        logger.info("Processing exception FourthMiddleware {}".format(request))


class MiddlewareManager(MiddlewareManagerBase):
    settings_key = "MIDDLEWARES_LIST"

    def _add_method(self, mw_cls):
        if hasattr(mw_cls, "process_request"):
            self.methods.append(mw_cls().process_request)
        if hasattr(mw_cls, "process_response"):
            self.methods.append(mw_cls().process_response)
        if hasattr(mw_cls, "process_exception"):
            self.methods.append(mw_cls().process_exception)


settings = {
    "MIDDLEWARES_LIST": {
        "__main__.FirstMiddleware": 0,
        "__main__.SecondMiddleware": 1,
        "__main__.ThirdMiddleware": 2,
        "__main__.FourthMiddleware": 3
    }
}

if __name__ == "__main__":
    manager = MiddlewareManager(settings=settings)
    manager.run()
