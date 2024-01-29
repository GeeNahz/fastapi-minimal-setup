from pydantic import EmailStr, BaseModel


class BasePassword(BaseModel):
    new_password: str


class PasswordChange(BasePassword):
    user_id: int
    old_password: str


class PasswordReset(BasePassword):
    token: str