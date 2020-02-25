from ..base import MiddlewareManagerBase


class MiddlewareManager(MiddlewareManagerBase):
    settings_key = "DOWNLOADER_MIDDLEWARES"

    def _add_method(self, mw_cls):
        if hasattr(mw_cls, "process_request"):
            self.methods['process_request'].append(mw_cls().process_request)
        if hasattr(mw_cls, "process_response"):
            self.methods['process_response'].append(mw_cls().process_response)
        if hasattr(mw_cls, "process_exception"):
            self.methods['process_exception'].append(mw_cls().process_exception)
