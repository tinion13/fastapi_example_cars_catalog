from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from core.consts import STATIC_DIR, TEMPLATES_DIR
from core.errors_pages_setup import setup_error_handlers
from core.master_router import router as master_router
from db.models import Base
from db.session import engine
from services.auth_service import AuthService


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    service = AuthService()
    app.state.service = service
    templates = Jinja2Templates(directory=TEMPLATES_DIR)
    app.state.templates = templates

    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan, title="Cars Catalog")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
setup_error_handlers(app)
app.include_router(master_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
