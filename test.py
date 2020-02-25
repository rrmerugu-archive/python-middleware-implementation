from middleware_manager.base import MiddlewareManagerBase
from middleware_manager import MiddlewareMixin
import logging
from middleware_manager.base import Request, Response


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class StartRequestMiddleware(MiddlewareMixin):

    def process_request(self, request=None):
        logger.info("Processing request {name} {request}".format(name=self.__class__.__name__, request=request))
        request.is_request_processed = True
        return request


class ComputeRequestMiddleware(MiddlewareMixin):

    def process_request(self, request=None):
        """
        if Response type is returned, then processing requests will be stopped.

        :param request:
        :return:
        """
        logger.info("Processing request {name} {request}".format(name=self.__class__.__name__, request=request))
        payload = request.payload
        return Response(payload['a'] * payload['b'])


class DefaultExceptionMiddleware(MiddlewareMixin):

    def process_exception(self, request=None, exception=None):
        logger.info("Processing exception {name} request:{request} exception:{exception}".format(
            name=self.__class__.__name__,
            request=request,
            exception=exception.__str__())
        )


class ResponseHandlerMiddleware(MiddlewareMixin):

    def process_response(self, request=None, response=None):
        logger.info("Processing response {name} request:{request} response:{response}".format(
            name=self.__class__.__name__,
            request=request,
            response=response)
        )


class MiddlewareManager(MiddlewareManagerBase):
    settings_key = "MIDDLEWARES_LIST"

    def _add_method(self, mw_cls):
        if hasattr(mw_cls, "process_request"):
            self.methods['process_request'].append(mw_cls().process_request)
        if hasattr(mw_cls, "process_response"):
            self.methods['process_response'].append(mw_cls().process_response)
        if hasattr(mw_cls, "process_exception"):
            self.methods['process_exception'].append(mw_cls().process_exception)


settings = {
    "MIDDLEWARES_LIST": {
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
