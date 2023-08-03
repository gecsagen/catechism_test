from typing import Optional


from pydantic import BaseModel


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class ShowCategory(TunedModel):
    """Модель отображения категории"""

    id: int
    name: str


class CategoryCreate(BaseModel):
    """Модель создания категории"""

    name: str


class DeleteCategoryResponse(BaseModel):
    """Модель удаления категории"""

    deleted_categiry_id: int


class UpdateCategoryResponse(BaseModel):
    """Модель обновления категории"""

    updated_category_id: int


class UpdateCategoryRequest(BaseModel):
    """Модель обновления категории"""

    name: Optional[str]


class ShowQuestion(TunedModel):
    """Модель отображения вопроса"""

    id: int
    text: str
    difficulty: int
    comment: str
    test_name: int


class QuestionCreate(BaseModel):
    """Модель создания вопроса"""

    text: str
    difficulty: int
    comment: str
    test_name: int


class DeleteQuestionResponse(BaseModel):
    """Модель удаления вопроса"""

    deleted_question_id: int


class UpdateQuestionResponse(BaseModel):
    """Модель обновления вопроса"""

    updated_question_id: int


class UpdateQuestionRequest(BaseModel):
    """Модель обновления вопроса"""

    text: Optional[str]
    difficulty: Optional[int]
    comment: Optional[str]
    test_name: Optional[int]
