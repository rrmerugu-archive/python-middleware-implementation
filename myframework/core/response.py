class Response:
    created_at = None
    result = None

    def __init__(self, result=None):
        self.result = result

    def __str__(self):
        return "<Response result={}>".format(self.result)
