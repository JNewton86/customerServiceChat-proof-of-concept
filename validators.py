from pydantic import BaseModel, Field, ValidationError
from exceptions import validate_with_model
from main import call_openai_api
from models import UserInput
from prompts import create_retry_prompt

def validate_user_input(input_data):
    try:
        user_input = UserInput(**input_data)
        return user_input
    except ValidationError as e:
        print(f"Validation error occured")
        for error in e.errors():
            print(f"Field: {error['loc'][0]}, Error: {error['msg']}")
        return None
    
def validate_llm_response(
    prompt, data_model, n_retry=5, model="gpt-4o"
):
    # Initial LLM call
    response_content = call_openai_api(prompt, model=model) # type: ignore
    current_prompt = prompt

    # Try to validate with the model
    # attempt: 0=initial, 1=first retry, ...
    for attempt in range(n_retry + 1):

        validated_data, validation_error = validate_with_model(
            data_model, response_content
        )

        if validation_error:
            if attempt < n_retry:
                print(f"retry {attempt} of {n_retry} failed, trying again...")
            else:
                print(f"Max retries reached. Last error: {validation_error}")
                return None, (
                    f"Max retries reached. Last error: {validation_error}"
                )

            validation_retry_prompt = create_retry_prompt(
                original_prompt=current_prompt,
                original_response=response_content,
                error_message=validation_error
            )
            response_content = call_openai_api(
                validation_retry_prompt, model=model # type: ignore
            )
            current_prompt = validation_retry_prompt
            continue

        # If you get here, both parsing and validation succeeded
        return validated_data, None