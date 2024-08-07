from fastapi import FastAPI, Body, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

users_db = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get("/")
def get_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users_db})


@app.get(path="/user/{user_id}")
def get_user(request: Request, user_id: int) -> HTMLResponse:
    try:
        for user in users_db:
            if user.id == user_id:
                return templates.TemplateResponse("users.html", {"request": request, "user": user})
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")


@app.post("/user/{username}/{age}")
def post_user(request: Request, user: User, username: str, age: int) -> HTMLResponse:
    if len(users_db) == 0:
        user.id = 1
        user.username = username
        user.age = age
        users_db.append(user)
        return templates.TemplateResponse("users.html", {"request": request, "user": user})
    user.id = int(max([i.id for i in users_db])) + 1
    user.username = username
    user.age = age
    users_db.append(user)
    return templates.TemplateResponse("users.html", {"request": request, "user": user})


@app.put("/user/{user_id}/{username}/{age}")
def update_user(user_id: int, username: str, age: int) -> str:
    try:
        for user in users_db:
            if user.id == user_id:
                user.username = username
                user.age = age
                return 'Пользователь добавлен'
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")
def delete_user(user_id: int) -> str:
    try:
        for user in users_db:
            if user.id == user_id:
                users_db.remove(user)
        return f"Пользователь {user_id} был удалён"
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")
