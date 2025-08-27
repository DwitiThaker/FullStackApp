from fastapi import FastAPI, Request, status
import models
from database import engine
from routers import auth, todos, admin, users
import os
#from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles 
from fastapi.responses import RedirectResponse

app = FastAPI()

# Creates tables if they don't exist; does not overwrite existing tables or data.
models.Base.metadata.create_all(bind=engine)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")


@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)  # ✅ fixed


@app.get("/healthy")
async def healthy():
    return {"status": "Healthy"}

# create_all() only creates missing tables; it does NOT modify existing tables.
# So if you change models (add columns), create_all() won’t update the tables automatically.
# For schema changes, it's often easier to delete the existing DB and recreate it during development.

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
