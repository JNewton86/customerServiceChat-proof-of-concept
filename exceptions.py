


# Define a custom exception for OpenAI API errors
from pydantic import ValidationError


class OpenAIAPIError(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"OpenAI API Error: {self.message}"
    
def validate_with_model(data_model, llm_response):
    try:
        validated_data = data_model.model_validate_json(llm_response)
        print("data validation successful!")
        print(validated_data.model_dump_json(indent=2))
        return validated_data, None
    except ValidationError as e:
        print(f"error validating data: {e}")
        error_message = (
            f"This response generated a validation error: {e}."
        )
        return None, error_message