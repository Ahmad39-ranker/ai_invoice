from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: str = Field(alias="_id")
    hashed_password: str
    role: str

    class Config:
        populate_by_name = True

class Token(BaseModel):
    access_token: str
    token_type: str

# This is the model for updating a user's role
class UserUpdateRole(BaseModel):
    role: str

class InvoiceInDB(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    filename: str
    upload_timestamp: str
    status: str
    data: Optional[Dict[str, Any]] = None

    class Config:
        populate_by_name = True

class PredictionResponse(BaseModel):
    vendor: str
    date: str = "N/A"
    amount: float = 0.0
    tax_id: str = "N/A"
    fraud_score: float = 0.0
    language: str = "en"