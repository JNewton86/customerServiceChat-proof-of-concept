import json
import os
from typing import Optional, Literal, List

import openai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import instructor
from pydantic import BaseModel, Field, ValidationError, EmailStr

from exceptions import OpenAIAPIError
from models import CustomerQuery as CustomerQuery, UserInput
from open_ai_calls import call_openai_api
from prompts import create_retry_prompt
from sampleUserInput import user_input_1
from validators import validate_user_input

app = FastAPI()

# home path
@app.get("/")
def root():
    return {"message": "Welcome to the Customer Support AI API!"}

# Define a route to handle user queries
@app.post("/query/")
async def handle_user_query(user_query: UserInput):
    
    try:
        user_input = validate_user_input(user_query)
        prompt = """Analyze this user query: {user_input} and provide a response in the properly formatted JSON object format matching this exact structure and data types: {example_response_Structure}
            respond ONLY with valid JSON. Do not include any eplanations or other text or formatting before or after the JSON object. """

        # Call the OpenAI API with the prompt
        response = await call_openai_api(prompt)
        
        if response is None:
            raise OpenAIAPIError("No response from OpenAI API")
        valid_data = CustomerQuery.model_validate_json(response) 

        return {"response": valid_data}
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except OpenAIAPIError as e:
        raise HTTPException(status_code=500, detail=str(e))



