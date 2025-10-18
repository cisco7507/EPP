class EPPError(Exception):
    """Base class for EPP client exceptions."""
    def __init__(self, message, code=None, response=None):
        super().__init__(message)
        self.code = code
        self.response = response

    def __str__(self):
        return f"EPP Error {self.code}: {self.message}"
