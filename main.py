
from pydantic import BaseModel, Field, ValidationError, EmailStr
import json
import openai
from typing import Optional, Literal, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
import prompt from prompts
from models import CustomerQuery as user_query

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Define the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the OpenAI model to use
MODEL = os.getenv("AI_MODEL")

# Define a custom exception for OpenAI API errors
class OpenAIAPIError(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"OpenAI API Error: {self.message}"

# Define a custom exception handler for OpenAI API errors
@app.exception_handler(OpenAIAPIError)
async def openai_api_error_handler(request, exc: OpenAIAPIError):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )

# Define a function to call the OpenAI API
async def call_openai_api(prompt: str) -> Optional[str]:
    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise OpenAIAPIError(str(e))
        
# Define a route to handle user queries
@app.post("/query/")
async def handle_user_query(user_query: "user_query"):
    try:
        # Convert the user query to a prompt
        prompt = f"User Query:\nName: {user_query.name}\nEmail: {user_query.email}\nQuery: {user_query.query}\nPriority: {user_query.priority}\nCategory: {user_query.category}\nIs Complaint: {user_query.is_complaint}\nTags: {', '.join(user_query.tags)}"
        
        # Call the OpenAI API with the prompt
        response = await call_openai_api(prompt)
        
        if response is None:
            raise OpenAIAPIError("No response from OpenAI API")
        
        return {"response": response}
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except OpenAIAPIError as e:
        raise HTTPException(status_code=500, detail=str(e))



