from pydantic import BaseModel


class LoginValidator(BaseModel):
    username: str
    password: str


class UserValidator(BaseModel):
    username: str
    email: str
    password: str


class PostValidator(BaseModel):
    title: str
    content: str


class CommentValidator(BaseModel):
    content: str
