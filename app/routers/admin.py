from fastapi import APIRouter, Depends, status, HTTPException, Response
from app.dependencies import get_current_admin_user
from app.models import UserInDB, InvoiceInDB, UserUpdateRole
from database.db import db
from bson import ObjectId

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/test")
async def admin_test(current_admin: UserInDB = Depends(get_current_admin_user)):
    return {"message": f"Welcome, admin {current_admin.username}!"}

@router.get("/invoices", response_model=list[InvoiceInDB])
async def get_all_invoices(current_admin: UserInDB = Depends(get_current_admin_user)):
    """
    Retrieves all invoices from the database.
    This endpoint is only accessible to users with the 'admin' role.
    """
    invoices = db.db.invoices.find({}).sort("upload_timestamp", -1)
    
    invoice_list = []
    async for doc in invoices:
        if "_id" in doc and isinstance(doc["_id"], ObjectId):
            doc["_id"] = str(doc["_id"])
        invoice_list.append(InvoiceInDB.model_validate(doc))
        
    return invoice_list

@router.get("/users", response_model=list[UserInDB])
async def get_all_users(current_admin: UserInDB = Depends(get_current_admin_user)):
    """
    Retrieves all users from the database.
    This endpoint is only accessible to users with the 'admin' role.
    """
    users = db.db.users.find({})
    user_list = []
    async for doc in users:
        if "_id" in doc and isinstance(doc["_id"], ObjectId):
            doc["_id"] = str(doc["_id"])
        user_list.append(UserInDB.model_validate(doc))
    return user_list

@router.put("/users/{user_id}", response_model=UserInDB)
async def update_user_role(user_id: str, new_role: UserUpdateRole, current_admin: UserInDB = Depends(get_current_admin_user)):
    """
    Updates a user's role.
    This endpoint is only accessible to users with the 'admin' role.
    """
    update_result = await db.db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"role": new_role.role}}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found or role is the same")

    updated_user = await db.db.users.find_one({"_id": ObjectId(user_id)})
    if "_id" in updated_user:
        updated_user["_id"] = str(updated_user["_id"])
    
    return UserInDB.model_validate(updated_user)

@router.delete("/invoices/{invoice_id}")
async def delete_invoice(invoice_id: str, current_admin: UserInDB = Depends(get_current_admin_user)):
    """
    Deletes an invoice by its ID.
    This endpoint is only accessible to users with the 'admin' role.
    """
    delete_result = await db.db.invoices.delete_one({"_id": ObjectId(invoice_id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    return {"message": "Invoice deleted successfully"}