from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from typing import Annotated
from pydantic import BaseModel

from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/")
def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get('/users/{user_id}')
async def get_users(request: Request, user_id: int) -> HTMLResponse:
    user = next((index for index, user in enumerate(users) if user.id == user_id), None)
    try:
        return templates.TemplateResponse("users.html", {"request": request, "user": users[user]})
    except IndexError:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")


@app.post('/user/{username}/{age}')
async def post_user(user: User) -> str:
    if users:
        user.id = max(users, key=lambda usr: usr.id).id + 1
    else:
        user.id = 1
    users.append(user)
    return f'User {user.id} has been registered.'


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(
        user_id: Annotated[int, Path(ge=1, description='Введите user_id (целое число)', example=1)],
        username: Annotated[
            str, Path(min_length=3, max_length=15, description='Введите имя_пользователя', example='DefaultUser')],
        age: Annotated[int, Path(ge=18, le=120, description='Введите Ваш возраст', example='39')]) -> str:
    user = next((index for index, user in enumerate(users) if user.id == user_id), None)
    try:
        users[user].username = username
        users[user].age = age
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")
    return f'User {user_id} has been updated.'


@app.delete('/user/{user_id}')
async def delete_user(
        user_id: Annotated[int, Path(ge=1, description='Введите user_id (целое число)', example=1)]) -> User:
    user = next((index for index, user in enumerate(users) if user.id == user_id), None)
    try:
        return users.pop(user)
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")
