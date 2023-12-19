from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.api_admin.routers import routers
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = '5895760296:AAF2hSRl3TAIrZGHD6M5sSDdtdYkQPr9sUc'


app = FastAPI(
    title="Envelope-app",
    version="1.0.0a",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url=None,
)

bot = Bot(token=TOKEN)
dp = Dispatcher()


ORIGINS = [
    "http://localhost",
    "http://localhost:5173",
    "https://envelope-app.ru",
    "https://www.envelope-app.ru",
    "https://store.envelope-app.ru",
    "https://api.telegram.org",
]


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=ORIGINS,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


for router in routers:
    app.include_router(router)


@app.post('/api/v1/webhook')
async def receive_update(request: Request):
    # Десериализация обновления Telegram
    update = await request.json()
    # Обновление диспетчера
    await dp.process_update(types.Update.to_object(update))
    return {'ok': True}


@dp.message(Command(commands=['/start']))
async def start(message: types.Message):
    await bot.send_message(message.chat.id, "Привет! Я ваш бот.")
