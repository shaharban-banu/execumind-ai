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

class CreateUserRequest(BaseModel):
    username: str
    email: str | None = None
    password: str


class UserManagementResponse(BaseModel):
    id: int
    username: str
    email: str | None = None
    role: str
    is_active: bool