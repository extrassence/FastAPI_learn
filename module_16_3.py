from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}


def next_id():
    print("Current users:", users)
    if not users:
        return 1
    return int(max(users)) + 1


@app.get('/users')
async def get_users() -> dict:
    return users


@app.post('/user/{username}/{age}')
async def post_user(username: Annotated[
    str, Path(min_length=3, max_length=15, description='Введите имя_пользователя', example='DefaultUser')],
                    age: Annotated[int, Path(ge=18, le=120, description='Введите Ваш возраст', example='30')]) -> str:
    user_id = next_id()
    users[str(user_id)] = f'Имя: {username}, возраст: {age}'
    return f'User {user_id} is registered.'


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(
        user_id: Annotated[int, Path(gt=0, description='Введите ID: ', example=10)],
        username: Annotated[
            str, Path(min_length=3, max_length=15, description='Введите имя пользователя', example='DefaultUser')],
        age: Annotated[int, Path(ge=18, le=120, description='Введите возраст', example='30')]) -> str:
    if str(user_id) not in list(users.keys()):
        return f'There is no user {user_id}'
    else:
        users[str(user_id)] = f'Имя: {username}, возраст: {age}'
    return f'User {user_id} has been updated.'


@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(gt=0, description='ID пользователя: ',
                                                   example=int(max(users, key=int)))]) -> str:
    if str(user_id) not in list(users.keys()):
        return f'There is no user {user_id}'
    else:
        users.pop(str(user_id))
    return f'User {user_id} has been deleted.'
