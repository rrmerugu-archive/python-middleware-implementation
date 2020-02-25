class Request:
    payload = None
    response = False
    is_response_processed = False

    def __init__(self, payload=None):
        self.payload = payload
