from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api_admin.routers import routers
import aiohttp


app = FastAPI(
    title="Envelope-app",
    version="1.0.0a",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url=None,
)


async def send_webhook(url):
    async with aiohttp.ClientSession() as session:
        payload = {"url": url}
        headers = {"Content-Type": "application/json"}

        async with session.post('https://api.telegram.org/bot6616951235:AAEcMXkGdXNTibeVr1j2zMu3CHLF1A8l_2A/setWebhook',
                                json=payload, headers=headers) as response:
            return await response.json()


@app.post("/")
async def test():
    ngrok_url = "https://envelope-app.ru"
    response = await send_webhook(ngrok_url)
    print(response)
    return {"ok": True}

# @app.post("/")
# async def test():
#     pass

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
