from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from app.schemas.question import QuestionOut, QuestionOutWithAnswer


# 基础试卷模型
class PaperBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)


# 创建试卷请求
class PaperCreate(PaperBase):
    question_ids: List[int] = Field(..., description="题目ID列表")


# 更新试卷请求
class PaperUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    question_ids: Optional[List[int]] = None
    status: Optional[str] = None


# 试卷列表响应
class PaperOut(PaperBase):
    id: int
    total_score: int
    status: str
    created_at: datetime
    published_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# 试卷详情响应(学生端)
class PaperDetailOut(PaperOut):
    questions: List[QuestionOut]


# 试卷详情响应(教师端)
class PaperDetailWithAnswerOut(PaperOut):
    questions: List[QuestionOutWithAnswer]


# 发布响应
class PaperPublishOut(BaseModel):
    id: int
    status: str
    published_at: datetime
    message: str = "试卷发布成功"

    class Config:
        from_attributes = True