class Life360Exception(Exception):
    """Base exception for Life360 MCP"""
    pass

class Life360AuthError(Life360Exception):
    """Authentication failed or missing token"""
    pass

class Life360APIError(Life360Exception):
    """API request failed"""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}")
