import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
import models
from openai import OpenAI
from auth import throttling, dependencies

load_dotenv(override=True)
app = FastAPI()

system_prompt = "Answer the user in plaintext (no markdown), but use lots of emojis. Be simple, clear and concise."
gemini_api_key = os.getenv("GEMINI_API_KEY")

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
gemini = OpenAI(base_url = GEMINI_BASE_URL, api_key = gemini_api_key)

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Add it to .env or your environment.")

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.post("/chat")
async def chat(request: models.ChatRequest, user_id: str = Depends(dependencies.get_user_identifier)):
    throttling.apply_rate_limit(user_id)

    response_text = gemini.chat.completions.create(model="gemini-3.1-flash-lite", 
                                                   messages=[{"role": "system", "content": system_prompt}, 
                                                             {"role": "user", "content": request.prompt}])
    return models.ChatResponse(response=response_text.choices[0].message.content)


# response = gemini.chat.completions.create(model="gemini-2.5-flash-lite", messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": request}])