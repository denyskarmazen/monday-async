class MondayQueryError(Exception):
    def __init__(self, message, original_errors=None):
        super().__init__(message)
        self.original_errors = original_errors or []


class GraphQLError(Exception):
    def __init__(self, message, original_errors=None):
        super().__init__(message)
        self.original_errors = original_errors or []