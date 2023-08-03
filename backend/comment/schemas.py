import datetime
from typing import Optional

from pydantic import BaseModel


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class ShowComment(TunedModel):
    """Модель отображения коммента"""

    id: int
    text: str
    user_id: int
    question_id: int
    created_at: datetime.datetime


class CommentCreate(BaseModel):
    """Модель создания коммента"""

    text: str
    user_id: int
    question_id: int


class DeleteCommentResponse(BaseModel):
    """Модель удаления коммента"""

    deleted_comment_id: int


class UpdateCommentResponse(BaseModel):
    """Модель обновления коммента"""

    updated_comment_id: int


class UpdateCommentRequest(BaseModel):
    """Модель обновления коммента"""

    text: Optional[str]
