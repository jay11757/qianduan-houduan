from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.paper import Paper, paper_question
from app.models.question import Question
from app.schemas.paper import PaperCreate, PaperUpdate


class PaperService:
    @staticmethod
    def create_paper(db: Session, paper_in: PaperCreate) -> Paper:
        """创建试卷，自动计算总分，保留题目顺序"""
        question_map = {q.id: q for q in db.query(Question).filter(Question.id.in_(paper_in.question_ids))}
        
        if len(question_map) != len(paper_in.question_ids):
            missing_ids = set(paper_in.question_ids) - set(question_map.keys())
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"题目不存在: {', '.join(map(str, missing_ids))}"
            )
        
        total_score = sum(q.score for q in question_map.values())
        
        db_paper = Paper(
            title=paper_in.title,
            description=paper_in.description,
            total_score=total_score,
            status="draft"
        )
        db.add(db_paper)
        db.commit()
        db.refresh(db_paper)
        
        for index, question_id in enumerate(paper_in.question_ids):
            db.execute(
                paper_question.insert().values(
                    paper_id=db_paper.id,
                    question_id=question_id,
                    sort_order=index
                )
            )
        db.commit()
        
        db.refresh(db_paper)
        return db_paper

    @staticmethod
    def get_paper_list(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: str | None = None,
        is_student: bool = False
    ) -> list[Paper]:
        """获取试卷列表"""
        query = db.query(Paper)
        
        if is_student:
            query = query.filter(Paper.status == "published")
        
        if status:
            query = query.filter(Paper.status == status)
        
        query = query.order_by(Paper.created_at.desc())
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_paper_by_id(db: Session, paper_id: int, is_teacher: bool = False) -> Paper:
        """根据ID获取试卷详情，按题目顺序返回"""
        db_paper = db.query(Paper).filter(Paper.id == paper_id).first()
        if not db_paper:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="试卷不存在"
            )
        
        if not is_teacher and db_paper.status != "published":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="该试卷尚未发布"
            )
        
        questions = db.query(Question).join(
            paper_question,
            Question.id == paper_question.c.question_id
        ).filter(
            paper_question.c.paper_id == paper_id
        ).order_by(
            paper_question.c.sort_order
        ).all()
        
        db_paper.questions = questions
        return db_paper

    @staticmethod
    def publish_paper(db: Session, paper_id: int) -> Paper:
        """发布试卷"""
        db_paper = db.query(Paper).filter(Paper.id == paper_id).first()
        if not db_paper:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="试卷不存在"
            )
        
        if db_paper.status == "published":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该试卷已经发布"
            )
        
        db_paper.status = "published"
        db_paper.published_at = datetime.utcnow()
        db.commit()
        db.refresh(db_paper)
        return db_paper