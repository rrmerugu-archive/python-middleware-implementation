from myframework.core.middleware.downloader.manager import MiddlewareManager
from myframework.core.middleware.downloader.mixins import DownloaderMiddlewareMixin

import logging
from myframework.core.response import  Response
from myframework.core.request import Request


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class StartRequestMiddleware(DownloaderMiddlewareMixin):

    def process_request(self, request=None):
        logger.info("Processing request {name} {request}".format(name=self.__class__.__name__, request=request))
        request.is_request_processed = True
        return request


class ComputeRequestMiddleware(DownloaderMiddlewareMixin):

    def process_request(self, request=None):
        """
        if Response type is returned, then processing requests will be stopped.

        :param request:
        :return:
        """
        logger.info("Processing request {name} {request}".format(name=self.__class__.__name__, request=request))
        payload = request.payload
        return Response(payload['a'] * payload['b'])


class DefaultExceptionMiddleware(DownloaderMiddlewareMixin):

    def process_exception(self, request=None, exception=None):
        logger.info("Processing exception {name} request:{request} exception:{exception}".format(
            name=self.__class__.__name__,
            request=request,
            exception=exception.__str__())
        )


class ResponseHandlerMiddleware(DownloaderMiddlewareMixin):

    def process_response(self, request=None, response=None):
        logger.info("Processing response {name} request:{request} response:{response}".format(
            name=self.__class__.__name__,
            request=request,
            response=response)
        )


settings = {
    "DOWNLOADER_MIDDLEWARES": {
        "__main__.StartRequestMiddleware": 0,
        "__main__.ComputeRequestMiddleware": 1,
        "__main__.DefaultExceptionMiddleware": 2,
        "__main__.ResponseHandlerMiddleware": 3,

    }
}

if __name__ == "__main__":
    example_task = Request(payload={"a": 5, "b": None})
    manager = MiddlewareManager(settings=settings)
    manager.run(request=example_task)
