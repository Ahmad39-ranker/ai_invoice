from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models import UserCreate, UserInDB, Token
from app.services import get_password_hash, verify_password, create_access_token
from database.db import db

router = APIRouter()

# app/routers/users.py
from fastapi import APIRouter, HTTPException, status
from app.models import UserCreate, UserInDB
from app.services import get_password_hash
from database.db import db
from pymongo.errors import DuplicateKeyError

router = APIRouter()

@router.post("/register", response_model=UserInDB)
async def register_user(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    new_user_data = user.model_dump()
    new_user_data["hashed_password"] = hashed_password
    new_user_data["role"] = "user"
    new_user_data.pop("password")

    try:
        # Attempt to insert the new user
        result = await db.db.users.insert_one(new_user_data)
        
        # Retrieve the newly created user document
        created_user = await db.db.users.find_one({"_id": result.inserted_id})
        
        # Explicitly convert the ObjectId to a string before passing to Pydantic
        if created_user:
            created_user["_id"] = str(created_user["_id"])
        
        # Return the validated model
        return UserInDB.model_validate(created_user)
    
    except DuplicateKeyError:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred during registration: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await db.db.users.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]}
    )
    # The fix is here:
    return {"access_token": access_token, "token_type": "bearer"}