from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users, prompts
from sqladmin import Admin
from app.admin import UserAdmin, PromptAdmin, authentication_backend
from app.db.db import engine

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router(users.router)
app.include_router(prompts.router)

# Initialize SQLAdmin
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(PromptAdmin)