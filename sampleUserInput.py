from models import UserInput

# Create a model instance for testing
user_input_1 = UserInput(
    name="John Doe",
    email="john.doe@example.com",
    query="I can't log into my account, I think my password is wrong.",
    order_id=12345,
    purchase_date="2023-10-15" # type: ignore
)
