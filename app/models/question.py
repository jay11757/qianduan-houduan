from sqlalchemy import Column, Integer, String, Text, DateTime, JSON  # 导入JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base
from app.models.paper import paper_question

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False, comment="题目内容")
    type = Column(String(50), nullable=False, comment="题目类型")
    options = Column(JSON, comment="选项列表，JSON格式")  # 改成JSON类型
    answer = Column(Text, comment="正确答案")
    score = Column(Integer, nullable=False, default=1, comment="题目分值")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联试卷
    papers = relationship("Paper", secondary=paper_question, back_populates="questions")