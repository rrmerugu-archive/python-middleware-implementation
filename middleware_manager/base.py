from middleware_manager.utils import import_class
from operator import itemgetter


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
    methods = []
    settings_key = None

    def __init__(self, settings=None):
        self.settings = settings
        self.validate_cls_settings()

        self.mw_classes = self.import_classes()
        # print(self.mw_classes)

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

    def run(self):
        for cls in self.mw_classes:
            self._add_method(cls)

        for method in self.methods:
            method()

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
