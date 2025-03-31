from .auth import decode_jwt_token, SECRET_KEY
from fastapi import status, HTTPException
from .db.models import User, Prompt, UserRole
from .db.db import get_session
from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend
from fastapi import Request
from app.auth import get_user_by_username, verify_password

# Define a custom authentication function for SQLAdmin
class SimpleAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        async for session in get_session():
            user = await get_user_by_username(username=username, db=session)
            if user and verify_password(password, user.hashed_password) and user.role == UserRole.ADMIN:
                request.session["user"] = username
                return True
        return False
    
    async def logout(self, request: Request) -> bool:
        request.session.pop("user", None)
        return True

    async def authenticate(self, request: Request):
        return request.session.get("user") is not None
    

authentication_backend = SimpleAuth(secret_key=SECRET_KEY)

# Create admin views for your models
class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.role]

class PromptAdmin(ModelView, model=Prompt):
    column_list = [Prompt.id, Prompt.input, Prompt.model_rating, Prompt.user_id]