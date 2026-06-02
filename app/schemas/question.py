from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# 基础题目模型（不含答案）
class QuestionBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000, description="题目内容")
    type: str = Field(..., description="题目类型: single/multiple/true_false/essay")
    options: Optional[List[str]] = Field(None, description="选项列表")
    score: int = Field(..., ge=1, description="题目分值")

# 创建题目请求
class QuestionCreate(QuestionBase):
    pass

# 更新题目请求
class QuestionUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1, max_length=2000)
    type: Optional[str] = None
    options: Optional[List[str]] = None
    answer: Optional[str] = None
    score: Optional[int] = Field(None, ge=1)

# 题目列表响应（不含答案，学生端用）
class QuestionOut(QuestionBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# 题目详情响应（含答案，教师端用）
class QuestionOutWithAnswer(QuestionOut):
    answer: Optional[str]

    class Config:
        from_attributes = True