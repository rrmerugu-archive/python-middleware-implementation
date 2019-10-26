from middleware_manager.manager import MiddlewareManager
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


settings = {
    "MIDDLEWARES_LIST": {
        "__main__.FirstMiddleware": 0,
        "__main__.SecondMiddleware": 1,
        "__main__.ThirdMiddleware": 2
    }
}

if __name__ == "__main__":
    manager = MiddlewareManager(settings=settings)
    manager.run()
