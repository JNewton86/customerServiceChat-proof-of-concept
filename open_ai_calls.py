# Define a function to call the OpenAI API
from typing import Optional
import openai
from exceptions import OpenAIAPIError
from models import CustomerQuery
from dotenv import load_dotenv
import os


load_dotenv()
ai_client = openai.OpenAI()
# Define the OpenAI API key and model
ai_client.api_key = os.getenv("OPENAI_API_KEY")  # type: ignore
ai_client.models = os.getenv("AI_MODEL", "gpt-3.5-turbo")    # type: ignore

async def call_openai_api(prompt: str) -> Optional[str]:
    try:
        response = ai_client.beta.chat.completions.parse(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            response_format=CustomerQuery
        )
        return response.choices[0].message.content
    except Exception as e:
        raise OpenAIAPIError(str(e))