from pydantic import BaseModel, Field, ValidationError, EmailStr
from datetime import date
from typing import Optional, Literal, List
import json

# Create a Pydantic model for validating customer support input
class UserInput(BaseModel):
    name: str
    email: EmailStr
    query: str
    order_id: Optional[int] = Field(
        None,
        description="5-digit order ID, if applicable, cannot start with 0",
        ge= 10000,
        le= 99999
    )
    purchase_date: Optional[date] = Field(
        None,
        description="Purchase date in YYYY-MM-DD format, if applicable"
     )
# Define the user query model   
class CustomerQuery(UserInput):
    priority: str = Field(..., description="Priority level: low, medium, high")
    category: Literal['refund_request', 'account', 'technical_support', 'informational_request', 'other']
    is_complaint: bool = Field(
        False,
        description="Whether the query is a complaint, default is False"
    )
    tags: list[str] = Field(
        default_factory=list,
        description="A list of tags associated with the query"
    )

# Define the Pydantic model for FAQ lookup arguments
class FAQLookupArgs(BaseModel):
    query: str = Field(..., description="user's query")
    tags: Optional[List[str]] = Field(
        default_factory=list,
        description="Relevant keyword tags from the customer's query"
    )

