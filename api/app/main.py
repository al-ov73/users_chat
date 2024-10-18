from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.auth import router as router_auth
from .routers.chat import router as router_chat
from .routers.users import router as router_users


app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["*"],
)

app.include_router(
    router_auth,
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    router_chat,
    prefix="/chat",
    tags=["chat"],
)

app.include_router(
    router_users,
    prefix="/users",
    tags=["users"],
)