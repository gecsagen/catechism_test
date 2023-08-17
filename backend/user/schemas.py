import re
import uuid
from typing import Optional

from pydantic import BaseModel
from pydantic import constr
from pydantic import EmailStr

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        from_attributes = True


class ShowUser(TunedModel):
    """Модель отображения пользователя"""

    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool


class UserCreate(BaseModel):
    """Модель создания пользователя"""

    name: str
    surname: str
    email: EmailStr
    password: str


class DeleteUserResponse(BaseModel):
    """Модель удаления пользователя"""

    deleted_user_id: uuid.UUID


class UpdatedUserResponse(BaseModel):
    """Модель ответа обновления пользователя"""

    updated_user_id: uuid.UUID


class UpdateUserRequest(BaseModel):
    """Модель обновления пользователя"""

    name: Optional[constr(min_length=1)]
    surname: Optional[constr(min_length=1)]
    email: Optional[EmailStr]


class Token(BaseModel):
    """Модель токена"""

    access_token: str
    token_type: str
