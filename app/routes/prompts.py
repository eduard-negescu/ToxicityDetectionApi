from fastapi import APIRouter, Depends, HTTPException, status
from model.model import predict
from app.auth import oauth2_scheme
from app.db.models import Prompt, User
from app.db.db import SessionDependency
from app.auth import decode_jwt_token
from sqlalchemy.future import select

router = APIRouter(prefix="/prompts")

@router.post("/")
async def post_prompt(input: str, db: SessionDependency, token: str = Depends(oauth2_scheme)):
    payload = decode_jwt_token(token)
    if "error" in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=payload["error"])
    
    model_rating = await predict(input)
    prompt = Prompt(
        user_id=int(payload["sub"]), 
        input=input,
        model_rating = model_rating
    )
    
    db.add(prompt)
    await db.commit()
    await db.refresh(prompt)
    return {"input": input, "model_rating": model_rating}

@router.get("")
async def get_prompts(db: SessionDependency, skip: int = 0, limit: int = 100, token: str = Depends(oauth2_scheme)):
    payload = decode_jwt_token(token)
    if "error" in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=payload["error"])
    
    user_id = int(payload["sub"])
    result = await db.execute(
        select(Prompt).where(Prompt.user_id == user_id).offset(skip).limit(limit)
    )
    prompts = result.scalars().all()
    return prompts
