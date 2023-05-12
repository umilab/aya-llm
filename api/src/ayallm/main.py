import sys
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from loguru import logger

from ayallm.routers.chat import chat_router
from ayallm.routers.model import model_router
from ayallm.models.settings import Settings
from ayallm.utils.convert import convert_all

# Configure logging settings

# Define a logger for the current mo
logger.add(sys.stderr, format="{time} {level} {message}", level="DEBUG")

settings = Settings()

tags_metadata = [
    {
        "name": "misc.",
        "description": "Miscellaneous endpoints that don't fit anywhere else",
    },
    {
        "name": "chats",
        "description": "Used to manage chats",
    },
]

description = """
Aya-LLM answers your questions poorly using LLaMA/alpaca. 🚀
"""

origins = [
    "http://localhost",
    "http://api:9124",
    "http://localhost:9123",
    "http://localhost:9124",
]

app = FastAPI(
    title="Aya-LLM", version="0.0.1", description=description, tags_metadata=tags_metadata
)

api_app = FastAPI(title="Aya-LLM API")
api_app.include_router(chat_router)
api_app.include_router(model_router)
app.mount("/api", api_app)

# handle serving the frontend as static files in production
if settings.NODE_ENV == "production":

    @app.middleware("http")
    async def add_custom_header(request, call_next):
        response = await call_next(request)
        if response.status_code == 404:
            return FileResponse("static/200.html")
        return response

    @app.exception_handler(404)
    def not_found(request, exc):
        return FileResponse("static/200.html")

    async def homepage(request):
        return FileResponse("static/200.html")

    app.route("/", homepage)
    app.mount("/", StaticFiles(directory="static"))

    start_app = app
else:
    start_app = api_app


@start_app.on_event("startup")
async def start_database():
    WEIGHTS = "/usr/src/app/weights/"
    files = os.listdir(WEIGHTS)
    files = list(filter(lambda x: x.endswith(".tmp"), files))

    for file in files:
        os.remove(WEIGHTS + file)

    logger.info("initializing models")
    convert_all("/usr/src/app/weights/", "/usr/src/app/weights/tokenizer.model")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
