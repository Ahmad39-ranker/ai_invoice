from fastapi import FastAPI
from app.routers import users, invoices, admin

app = FastAPI(
    title="Invoice AI Backend",
    description="A backend for a multilingual invoice automation platform.",
    version="1.0.0"
)

app.include_router(users.router, tags=["users"])
app.include_router(invoices.router)
app.include_router(admin.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Invoice AI API"}

# # Create a mock data folder for testing
# import os
# if not os.path.exists("mock_data"):
#     os.makedirs("mock_data")
#     with open("mock_data/ocr_response.json", "w") as f:
#         f.write('{"raw_text": "This is a mock invoice text. Total: $500", "extracted_fields": {"vendor": "Test Vendor"}}')