from fastapi import FastAPI, Path, HTTPException
from typing import Annotated
from pydantic import BaseModel
from typing import List

app = FastAPI()

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/users')
async def get_users() -> List[User]:
    return users


@app.post('/user/{username}/{age}')
async def post_user(user: User) -> str:
    if users:
        user.id = max(users, key=lambda usr: usr.id).id + 1
    else:
        user.id = 1
    users.append(user)
    return f'User {user.id} has been registered.'


@app.put('/user/{user_id}/{username}/{age}')
async def put_user(user_id: Annotated[int, Path(ge=1, description='Введите ID', example=1)],
                   username: Annotated[str, Path(min_length=3, max_length=15, description='Введите имя пользователя',
                                                 example='DefaultUser')],
                   age: Annotated[int, Path(ge=18, le=120, description='Введите возраст', example='30')]) -> User:
    user = next((index for index, user in enumerate(users) if user.id == user_id), None)
    try:
        users[user].username = username
        users[user].age = age
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user]


@app.delete('/user/{user_id}')
async def delete_user(
        user_id: Annotated[int, Path(ge=1, description='Введите ID', example=1)]) -> User:
    user = next((index for index, user in enumerate(users) if user.id == user_id), None)
    try:
        return users.pop(user)
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")
