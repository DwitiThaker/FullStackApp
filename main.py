from fastapi import FastAPI, Request, status
import models
from database import engine
from routers import auth, todos, admin, users
import os
from pathlib import Path

# templates and static handling
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

# Creates tables if they don't exist; does not overwrite existing tables or data.
models.Base.metadata.create_all(bind=engine)

BASE_DIR = Path(__file__).resolve().parent

# TEMPLATES (safe absolute path)
templates_path = BASE_DIR / "templates"
if templates_path.exists() and templates_path.is_dir():
    templates = Jinja2Templates(directory=str(templates_path))
else:
    # define a fallback templates variable to prevent errors elsewhere
    templates = None

# STATIC FILES (mount only if directory exists)
static_path = BASE_DIR / "static"
if static_path.exists() and static_path.is_dir():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")


@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)  # ✅ fixed


# create_all() only creates missing tables; it does NOT modify existing tables.
# So if you change models (add columns), create_all() won’t update the tables automatically.
# For schema changes, it's often easier to delete the existing DB and recreate it during development.

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
