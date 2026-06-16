from fastapi import HTTPException

class NotFoundException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=404, detail=detail)

class UnauthorizedException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=401, detail=detail)

class AlreadyExistsException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=409, detail=detail)