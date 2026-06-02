from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.paper import (
    PaperCreate,
    PaperOut,
    PaperDetailOut,
    PaperDetailWithAnswerOut,
    PaperPublishOut
)
from app.services.paper_service import PaperService

router = APIRouter(prefix="/papers", tags=["试卷管理"])

@router.post(
    "",
    response_model=PaperOut,
    status_code=status.HTTP_201_CREATED,
    # dependencies=[Depends(require_teacher)],
    summary="创建试卷"
)
def create_paper(
    paper_in: PaperCreate,
    db: Session = Depends(get_db)
):
    """
    创建新试卷
    - 接收题目ID数组，自动计算总分
    - 初始状态为草稿(draft)
    """
    return PaperService.create_paper(db, paper_in)

@router.get(
    "",
    response_model=List[PaperOut],
    summary="获取试卷列表"
)
def get_papers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    status: Optional[str] = Query(None, description="筛选状态: draft/published"),
    db: Session = Depends(get_db)
    # current_user: User = Depends(get_current_user)
):
    """
    获取试卷列表
    - 暂时关闭权限，所有人都能看到所有试卷
    """
    # 临时注释掉学生/教师判断，先测试功能
    # is_student = not current_user.is_teacher
    is_student = False
    return PaperService.get_paper_list(db, skip, limit, status, is_student)

@router.get(
    "/{paper_id}",
    response_model=PaperDetailOut,
    summary="获取试卷详情(学生端)"
)
def get_paper_detail(
    paper_id: int,
    db: Session = Depends(get_db)
    # current_user: User = Depends(get_current_user)
):
    """
    获取试卷详情，包含题目信息(不含答案)
    """
    return PaperService.get_paper_by_id(db, paper_id, is_teacher=False)

@router.get(
    "/{paper_id}/teacher",
    response_model=PaperDetailWithAnswerOut,
    # dependencies=[Depends(require_teacher)],
    summary="获取试卷详情(教师端)"
)
def get_paper_detail_teacher(
    paper_id: int,
    db: Session = Depends(get_db)
):
    """
    获取试卷详情，包含题目信息和答案
    """
    return PaperService.get_paper_by_id(db, paper_id, is_teacher=True)

@router.patch(
    "/{paper_id}/publish",
    response_model=PaperPublishOut,
    # dependencies=[Depends(require_teacher)],
    summary="发布试卷"
)
def publish_paper(
    paper_id: int,
    db: Session = Depends(get_db)
):
    """
    发布试卷
    - 将状态从draft改为published
    - 发布后学生才能看到
    """
    return PaperService.publish_paper(db, paper_id)