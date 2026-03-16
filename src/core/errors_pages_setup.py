from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

from core.consts import IMPLEMENTED_ERROR_TEMPLATES


def setup_error_handlers(app):

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request,
        exception: StarletteHTTPException,
    ) -> HTMLResponse:
        templates: Jinja2Templates = request.app.state.templates

        status_code = exception.status_code
        context = {
            "request": request,
            "detail": exception.detail,
            "status_code": status_code,
            "exc_type": "StarletteHTTPException",
        }
        headers = dict(exception.headers or {})

        response = templates.TemplateResponse(
            f"errors/{status_code if status_code in IMPLEMENTED_ERROR_TEMPLATES else 'http_error'}.html",
            context,
            status_code=status_code,
        )

        response.headers.update(headers)
        return response

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exception: RequestValidationError,
    ) -> HTMLResponse:
        templates: Jinja2Templates = request.app.state.templates
        context = {
            "request": request,
            "detail": exception.errors(),
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "exc_type": "RequestValidationError"
        }
        return templates.TemplateResponse(
            "errors/422.html",
            context,
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exception: Exception,
    ) -> HTMLResponse:
        templates: Jinja2Templates = request.app.state.templates
        context = {
            "request": request,
            "detail": str(exception),
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "exc_type": "Exception"
        }
        return templates.TemplateResponse(
            "errors/500.html",
            context,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
