from pydantic import BaseModel

class LoginRequest(BaseModel):
    username:str
    password:str

class UserResponse(BaseModel):
    """
    Authenticated user information.
    """
    username: str

class TokenResponse(BaseModel):
    access_token:str
    token_type:str="bearer"
    user: UserResponse