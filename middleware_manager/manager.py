"""


"""
from middleware_manager.utils import import_class
from operator import itemgetter


class MiddlewareManager:
    name = "MiddlewareManager"
    mw_classes = []  # classes
    methods = []  # methods to execute from the classes

    def __init__(self, settings=None):
        self.settings = settings
        self.mw_classes = self.import_classes()
        # print(self.mw_classes)

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
        _list = self.settings['MIDDLEWARES_LIST']
        ordered_list = {}
        for key, value in sorted(_list.items(), key=itemgetter(1), reverse=False):
            ordered_list[key] = value
        return ordered_list

    def _add_method(self, mw_cls):
        if hasattr(mw_cls, "process_request"):
            self.methods.append(mw_cls().process_request)
        if hasattr(mw_cls, "process_response"):
            self.methods.append(mw_cls().process_response)
        if hasattr(mw_cls, "process_exception"):
            self.methods.append(mw_cls().process_exception)

    def run(self):
        for cls in self.mw_classes:
            self._add_method(cls)

        for method in self.methods:
            method()
