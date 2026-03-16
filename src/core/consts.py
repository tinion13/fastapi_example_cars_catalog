from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "web" / "templates"
STATIC_DIR = BASE_DIR / "web" / "static"
CARS_PER_PAGE = 40
IMPLEMENTED_ERROR_TEMPLATES = {401, 403, 404, 422, 500}
COOKIE_NAME = "access_token"
