from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.db.db import SessionDependency
from app.db.models import User
from app.schemas.user_schemas import UserCreate
from app.auth import hash_password, verify_password, create_jwt_token, get_user_by_username

router = APIRouter(prefix="/users")

async def create_user(db: SessionDependency, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return "user created"

@router.post("/register")
async def register_user(user: UserCreate, db: SessionDependency):
    db_user = await get_user_by_username(user.username, db)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username taken"
        )
    return await create_user(db, user)

@router.post("/token")
async def login_for_access_token(db: SessionDependency, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_by_username(form_data.username, db)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    token = create_jwt_token({
        "sub": str(user.id),
        "role": user.role.value
    })
    return {"access_token": token, "token_type": "bearer"}
