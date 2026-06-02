from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

# 试卷-题目 关联表
paper_question = Table(
    "paper_question",
    Base.metadata,
    Column("paper_id", Integer, ForeignKey("papers.id"), primary_key=True),
    Column("question_id", Integer, ForeignKey("questions.id"), primary_key=True),
    Column("sort_order", Integer, default=0)  # 题目在试卷中的顺序
)

class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, comment="试卷标题")
    description = Column(String(1000), nullable=True, comment="试卷描述")
    total_score = Column(Integer, nullable=False, default=0, comment="试卷总分")
    status = Column(String(20), nullable=False, default="draft", comment="状态: draft(草稿)/published(已发布)")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime, nullable=True)
    
    # 关联题目
    questions = relationship("Question", secondary=paper_question, back_populates="papers")
    # 关联考试记录
    # exams = relationship("Exam", back_populates="paper")