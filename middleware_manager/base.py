from middleware_manager.utils import import_class, try_except
from operator import itemgetter


class Request:
    payload = None
    response = False
    is_response_processed = False

    def __init__(self, payload=None):
        self.payload = payload


class Response:
    created_at = None
    result = None

    def __init__(self, result=None):
        self.result = result

    def __str__(self):
        return "<Response result={}>".format(self.result)


class MiddlewareMixin:
    """

Example usage:

    def process_request(self, request=None):
        pass

    def process_response(self, request=None, response=None):
        pass

    def process_exception(self, request=None, response=None):
        pass
    """


class MiddlewareManagerBase:
    """

    implement settings_key = EXAMPLE_NAME




    """
    mw_classes = []  # classes
    methods = {
        "process_request": [],
        "process_response": [],
        "process_exception": [],
    }
    settings_key = None

    def __init__(self, settings=None):
        self.settings = settings
        self.validate_cls_settings()

        self.mw_classes = self.import_classes()
        print(self.mw_classes)

    def validate_cls_settings(self):
        if self.settings_key is None:
            raise Exception("Please give a key using which middleware classes "
                            "can be imported from settings. example `MIDDLEWARES_LIST`. ")

    def import_classes(self):
        mw_classes = []
        classes_list = self.load_settings()
        for cls, _ in classes_list.items():
            _cls = import_class(cls)
            if _cls is None:
                raise ImportError("Failed to import {} ".format(_cls))
            mw_classes.append(_cls)
        return mw_classes

    def load_settings(self):
        _list = self.settings[self.settings_key]
        ordered_list = {}
        for key, value in sorted(_list.items(), key=itemgetter(1), reverse=False):
            ordered_list[key] = value
        return ordered_list

    def run(self, request=None):
        for cls in self.mw_classes:
            self._add_method(cls)

        response = None
        exception = None
        for method in self.methods['process_request']:
            response, exception = try_except(method, request=request)
            if response is not None and not isinstance(response, (Response, Request)):
                raise ValueError('Middleware %s.process_request must return None, Response or Request, got %s' % \
                                 (method.__self__.__class__.__name__, response.__class__.__name__))
            print("response", response)
            if exception:
                break
        if exception:
            for _method in self.methods['process_exception']:
                try_except(_method, request=request, exception=exception)
        if response:
            for method in self.methods['process_response']:
                method(request=request, response=response)

    def _add_method(self, mw_cls):
        raise NotImplementedError("""
Example implementation:
        
def _add_method(self, mw_cls):
    if hasattr(mw_cls, "process_request"):
        self.methods.append(mw_cls().process_request)
    if hasattr(mw_cls, "process_response"):
        self.methods.append(mw_cls().process_response)
    if hasattr(mw_cls, "process_exception"):
        self.methods.append(mw_cls().process_exception)
    
        
        """)
