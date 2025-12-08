from typing import List

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserSchema(UserBase):
    password: str


class UserPublic(UserBase):
    id: int


class UserDB(UserSchema):
    id: int

    model_config = {'from_attributes': True}


class UserList(BaseModel):
    users: List[UserPublic]
