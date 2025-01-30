import logging

import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes import router

log = logging.getLogger("uvicorn")


app = FastAPI(
    title="Metis API",
    version="1.0.0",
    swagger_ui_init_oauth={"clientId": settings.KEYCLOAK_CLIENT_ID},
    docs_url=None,
    redoc_url=None,
)

origins = settings.CORS_ALLOW_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=origins,
)

app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")
