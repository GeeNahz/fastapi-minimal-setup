from pydantic import EmailStr, BaseModel


class EmailChangePassword(BaseModel):
    email: list[EmailStr]


class EmailPayload(BaseModel):
    email: EmailStr


class EmailData(BaseModel):
    email: list[EmailStr]
    body: "EmailBody"


# class EmailPassword(BaseEmail):
#     body: "EmailBody"


class EmailBody(BaseModel):
    token: str
    username: str


EmailData.model_rebuild()
