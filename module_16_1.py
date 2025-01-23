from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def main():
    return "Главная страница"


@app.get('/admin')
async def admin():
    return "Вы вошли как администратор"


@app.get('/user/{user_id}')
async def user(user_id):
    return f'Вы вошли как пользователь № {user_id}'


@app.get('/user')
async def news(username: str, age: int):
    return f'Информация о пользователе. Имя: {username}, Возраст: {age}'
