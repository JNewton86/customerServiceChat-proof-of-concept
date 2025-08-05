


# Define initial prompt for OpenAI API 
prompt = """Analyze this user query: {user_query} and provide a response in the properly formatted JSON in the format of this example:
{
    "name": "Example User",
    "email": "example.user@example.com",
    "query": "I can't log into my account, i think my password is wrong.",
    "priority": 3,
    "category": "account",
    "is_complaint": true,
    "tags": ["login", "password", "account"],
} """