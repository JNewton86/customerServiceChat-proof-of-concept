
# Define the Pydantic model for user query validation

# Define the user query model   
class CustomerQuery(BaseModel):
    name: str = Field(..., description="The name of the user")
    email: str = Field(..., description="The email address of the user")
    query: str = Field(..., description="The query string for the user")
    priority: str = Field(..., description="The priority of the query")
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