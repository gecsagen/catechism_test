import datetime

from pydantic import BaseModel


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class ShowHistory(TunedModel):
    """Модель отображения истории"""

    id: int
    user_id: int
    test_name: str
    created_at: datetime.datetime
    percentage_correct: float
    grade: int


class HistoryCreate(BaseModel):
    """Модель создания истории"""

    user_id: int
    test_name: str
    percentage_correct: float
    grade: int


class DeleteHistoryResponse(BaseModel):
    """Модель удаления истории"""

    deleted_history_id: int
