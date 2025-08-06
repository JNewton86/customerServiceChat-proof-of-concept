

# Example response structure for the OpenAI API
example_response_Structure = f"""{{
    "name": "Example User",
    "email": "example.user@example.com",
    "query": "I can't log into my account, i think my password is wrong.",
    "priority": 3,
    "category": "account",
    "is_complaint": true,
    "tags": ["login", "password", "account", "support", "exchange"],
}}"""


def create_retry_prompt(
    original_prompt, original_response, error_message
):
    retry_prompt = f"""
This is a request to fix an error in the structure of an llm_response.
Here is the original request:
<original_prompt>
{original_prompt}
</original_prompt>

Here is the original llm_response:
<llm_response>
{original_response}
</llm_response>

This response generated an error: 
<error_message>
{error_message}
</error_message>

Compare the error message and the llm_response and identify what 
needs to be fixed or removed
in the llm_response to resolve this error. 

Respond ONLY with valid JSON. Do not include any explanations or 
other text or formatting before or after the JSON string.
"""
    return retry_prompt