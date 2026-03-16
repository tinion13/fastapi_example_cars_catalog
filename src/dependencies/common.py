from fastapi import Request
from fastapi.templating import Jinja2Templates

from services.auth_service import AuthService


def get_service(request: Request) -> AuthService:
    return request.app.state.service


def get_templates(request: Request) -> Jinja2Templates:
    return request.app.state.templates
