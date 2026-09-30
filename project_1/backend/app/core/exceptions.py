from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class ExamRAGException(Exception):
    """Base application exception."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code


async def examrag_exception_handler(request: Request, exc: ExamRAGException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ExamRAGException, examrag_exception_handler)
