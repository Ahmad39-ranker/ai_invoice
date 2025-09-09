# from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
# from app.models import InvoiceInDB, PredictionResponse
# from app.dependencies import get_current_user
# from database.db import db
# from datetime import datetime
# import json
# import os
# from bson import ObjectId

# router = APIRouter(prefix="/invoices", tags=["invoices"])

# MOCK_OCR_RESPONSE_FILE = "mock_data/ocr_response.json"
# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Mock data for OCR and prediction
# def get_mock_ocr_data():
#     if not os.path.exists(MOCK_OCR_RESPONSE_FILE):
#         return {"raw_text": "Mock invoice text here.", "extracted_fields": {}}
#     with open(MOCK_OCR_RESPONSE_FILE, "r") as f:
#         return json.load(f)

# @router.post("/upload")
# async def upload_invoice(file: UploadFile = File(...), current_user=Depends(get_current_user)):
#     filename = file.filename
#     file_path = os.path.join(UPLOAD_FOLDER, filename)
#     with open(file_path, "wb") as buffer:
#         buffer.write(await file.read())

#     invoice_data = {
#         "user_id": current_user.id,
#         "filename": filename,
#         "upload_timestamp": datetime.utcnow().isoformat(),
#         "status": "uploaded"
#     }
    
#     result = await db.db.invoices.insert_one(invoice_data)
    
#     mock_ocr_data = get_mock_ocr_data()
    
#     await db.db.invoices.update_one(
#         {"_id": result.inserted_id},
#         {"$set": {"status": "processed", "data": mock_ocr_data}}
#     )

#     # Fetch the final invoice to return a consistent model
#     final_invoice = await db.db.invoices.find_one({"_id": result.inserted_id})
#     if "_id" in final_invoice:
#         final_invoice["_id"] = str(final_invoice["_id"])
    
#     return InvoiceInDB.model_validate(final_invoice)

# @router.post("/predict/{invoice_id}", response_model=PredictionResponse)
# async def get_prediction(invoice_id: str, current_user=Depends(get_current_user)):
#     # Retrieve the processed data from the database
#     invoice_doc = await db.db.invoices.find_one({
#         "_id": ObjectId(invoice_id),
#         "user_id": current_user.id
#     })
    
#     if not invoice_doc:
#         raise HTTPException(
#             status_code=404,
#             detail="Invoice not found or you do not have permission to view it."
#         )

#     # Use the mock data stored in the database
#     data = invoice_doc.get("data", {})
#     extracted_fields = data.get("extracted_fields", {})

#     return PredictionResponse(
#         vendor=extracted_fields.get("vendor", "N/A"),
#         date=extracted_fields.get("date", "N/A"),
#         amount=extracted_fields.get("amount", 0.0),
#         tax_id="N/A",  # You can add this to your mock data if needed
#         fraud_score=0.0,
#         language="en"
#     )

# @router.get("/history", response_model=list[InvoiceInDB])
# async def get_user_invoices(current_user=Depends(get_current_user)):
#     invoices = db.db.invoices.find({"user_id": current_user.id}).sort("upload_timestamp", -1)
    
#     # Corrected list comprehension to handle ObjectId validation
#     invoice_list = []
#     async for doc in invoices:
#         if "_id" in doc and isinstance(doc["_id"], ObjectId):
#             doc["_id"] = str(doc["_id"])
#         invoice_list.append(InvoiceInDB.model_validate(doc))
        
#     return invoice_list

import os
import json
import random
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from app.models import InvoiceInDB, PredictionResponse
from app.dependencies import get_current_user
from database.db import db
from bson import ObjectId


router = APIRouter(prefix="/user", tags=["user"])

MOCK_OCR_RESPONSE_FILE = "mock_data/ocr_response.json"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Mock data for OCR and prediction
def get_mock_ocr_data():
    if not os.path.exists(MOCK_OCR_RESPONSE_FILE):
        return {"raw_text": "Mock invoice text here.", "extracted_fields": {}}
    with open(MOCK_OCR_RESPONSE_FILE, "r") as f:
        return json.load(f)

@router.post("/upload")
async def upload_invoice(file: UploadFile = File(...), current_user=Depends(get_current_user)):
    filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    invoice_data = {
        "user_id": current_user.id,
        "filename": filename,
        "upload_timestamp": datetime.utcnow().isoformat(),
        "status": "uploaded"
    }
    
    result = await db.db.invoices.insert_one(invoice_data)
    
    mock_ocr_data = get_mock_ocr_data()
    
    await db.db.invoices.update_one(
        {"_id": result.inserted_id},
        {"$set": {"status": "processed", "data": mock_ocr_data}}
    )

    final_invoice = await db.db.invoices.find_one({"_id": result.inserted_id})
    if "_id" in final_invoice:
        final_invoice["_id"] = str(final_invoice["_id"])
    
    return InvoiceInDB.model_validate(final_invoice)

@router.post("/predict/{invoice_id}", response_model=PredictionResponse)
async def get_prediction(invoice_id: str, current_user=Depends(get_current_user)):
    invoice_doc = await db.db.invoices.find_one({
        "_id": ObjectId(invoice_id),
        "user_id": current_user.id
    })
    
    if not invoice_doc:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found or you do not have permission to view it."
        )

    data = invoice_doc.get("data", {})
    extracted_fields = data.get("extracted_fields", {})
    
    # Add a randomized fraud score to meet the objective
    fraud_score = random.uniform(0.01, 0.99)
    
    return PredictionResponse(
        vendor=extracted_fields.get("vendor", "N/A"),
        date=extracted_fields.get("date", "N/A"),
        amount=extracted_fields.get("amount", 0.0),
        tax_id="N/A",
        fraud_score=fraud_score,
        language="en"
    )


@router.get("/invoices", response_model=list[InvoiceInDB])
async def get_user_invoices(current_user=Depends(get_current_user)):
    invoices = db.db.invoices.find({"user_id": current_user.id}).sort("upload_timestamp", -1)
    
    invoice_list = []
    async for doc in invoices:
        if "_id" in doc and isinstance(doc["_id"], ObjectId):
            doc["_id"] = str(doc["_id"])
        invoice_list.append(InvoiceInDB.model_validate(doc))
        
    return invoice_list