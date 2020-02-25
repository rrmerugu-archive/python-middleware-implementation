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

    methods = {
        "process_request": [],
        "process_response": [],
        "process_exception": [],
    }
