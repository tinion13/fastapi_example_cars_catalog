from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from db.models import User
from dependencies.common import get_templates
from dependencies.policies import require_admin

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def admin_index(
    request: Request,
    admin: User = Depends(require_admin),
    templates: Jinja2Templates = Depends(get_templates)
):
    return templates.TemplateResponse(
        "admin/index.html",
        {"request": request, "admin": admin})
