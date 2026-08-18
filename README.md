# FastAPI Gemini OpenAI Proxy

A lightweight **FastAPI** backend that acts as an AI chat endpoint leveraging the **Gemini API** via **OpenAI's Python SDK compatibility layer**.

It includes built-in JWT authentication parsing and a dynamic rate-limiting mechanism to handle both authenticated users and guest access safely.

---

## Features

* **FastAPI Backend:** Fast, modern, and asynchronous web framework.
* **OpenAI SDK Integration:** Uses the official `openai` Python SDK redirected to Google's Gemini base URL.
* **JWT Authentication:** Optional Bearer token authentication via standard OAuth2 JWT tokens.
* **Tiered Throttling/Rate Limiting:**
  * **Unauthenticated (Global Guest):** 3 requests per 60 seconds.
  * **Authenticated:** 5 requests per 60 seconds per user.
* **Configurable system prompt:** Built in with a pre-configured system prompt designed for plain-text, concise, and emoji-friendly answers.

---

## Project Structure
```text
.
├── auth/
│   ├── dependencies.py  # JWT authentication dependencies
│   └── throttling.py    # Custom rate-limiting implementation
├── main.py              # Main application instance and /chat route setup
└── models.py            # Pydantic schemas for request and response validation
```
---

## Prerequisites
* Python 3.9+
* A valid Gemini API Key from Google AI Studio

---

## Installation and Setup

1. Clone the repository 

2. Create and activate a virtual environment (optional)
* python -m venv .venv
    * On macOS/Linux:
        source .venv/bin/activate
    * On Windows:
        .venv\Scripts\activate.ps1

3. Install the dependencies
* pip install fastapi uvicorn python-dotenv openai python-jose

4. Quick .env configuration
* Create a .env file in the root directory of the project and add your Gemini API Key as in the example below: 
    GEMINI_API_KEY="your_actual_gemini_api_key_here"

---
## Running the application
Start a local server using the command below: 

    uvicorn main:app --reload

The server will be available at http://127.0.0.1:8000

* Once the server is running, the endpoints can be tested directly in your browser either with Swagger UI or ReDoc:
    * Swagger UI: http://127.0.0.1:8000/docs
    * ReDoc: http://127.0.0.1:8000/redoc

---

## Available API Endpoints
* **GET "/"**
    * Verifies that the service is active

* **POST "/chat"**
    * Sends a prompt to the Gemini model using OpenAI's SDK integration.
    * Headers (Optional, for JWT Auth)
        * Authorization: Bearer (your_jwt_token)
    * Request body:
    ```json
        {
        "prompt": "Hello! What can you do?"
        }
    ```
    * Response body:
    ```json
        {
        "response": "I can chat with you and answer questions! 🤖✨ Simple and clear! 😄💬"
        }
    ```

---

## Rate Limiting
* Rate limit can be modified in throttling.py
*By default, it is set to 3 requests / 60s for guests and 5 requests / 60s for authenticated users with JWT token