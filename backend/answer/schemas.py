from typing import Optional

from pydantic import BaseModel


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class ShowAnswer(TunedModel):
    """Модель отображения ответа"""

    id: int
    text: str
    is_right: bool
    question_id: int


class AnswerCreate(BaseModel):
    """Модель создания ответа"""

    text: str
    is_right: bool
    question_id: int


class DeleteAnswerResponse(BaseModel):
    """Модель удаления ответа"""

    deleted_answer_id: int


class UpdateAnswerResponse(BaseModel):
    """Модель обновления ответа"""

    updated_answer_id: int


class UpdateAnswerRequest(BaseModel):
    """Модель обновления ответа"""

    text: Optional[str]
    is_right: Optional[bool]
    question_id: Optional[int]


class ShowUserAnswer(TunedModel):
    """Модель отображения ответа пользователя"""

    id: int
    user_id: int
    question_id: int
    answer_id: int
    history_id: int


class UserAnswerCreate(BaseModel):
    """Модель создания ответа пользователя"""

    user_id: int
    question_id: int
    answer_id: int
    history_id: int


class DeleteUserAnswerResponse(BaseModel):
    """Модель удаления ответа пользователя"""

    deleted_user_answer_id: int
