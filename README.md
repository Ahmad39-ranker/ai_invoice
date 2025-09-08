# Invoice AI Backend

This is the backend infrastructure for the Invoice AI platform, built with FastAPI and MongoDB.

## Features
- **User Authentication**: Register, login, and logout with JWT-based authentication.
- **Invoice Upload**: Upload PDF or image files. Metadata is stored in MongoDB.
- **Simulated Predictions**: Endpoints to simulate OCR and AI-based field extraction.
- **Invoice History**: View a user's uploaded invoices.
- **Admin Endpoints**: Manage users and invoices (admin-only).

## Tech Stack
- **Python 3.10+**
- **FastAPI**: For building the RESTful API.
- **MongoDB**: The NoSQL database for storing data.
- **PyMongo/Motor**: Asynchronous drivers for MongoDB.
- **JWT**: For user authentication.

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-repo/invoice_ai.git](https://github.com/your-repo/invoice_ai.git)
    cd invoice_ai
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the root directory.
    ```
    MONGO_URI=mongodb://localhost:27017
    MONGO_DB_NAME=invoice_ai
    JWT_SECRET_KEY=your_super_secret_key
    ```
    Make sure MongoDB is running on your machine.

5.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```
    The server will be running on `http://127.0.0.1:8000`.

## API Documentation
The interactive API documentation (Swagger UI) is available at `http://127.0.0.1:8000/docs`.