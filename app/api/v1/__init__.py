from fastapi import APIRouter

# 只导入已经写好的papers路由
from app.api.v1.papers import router as papers_router

# 其他空文件的导入先注释掉，以后写好了再取消注释
# from app.api.v1.auth import router as auth_router
# from app.api.v1.questions import router as questions_router
# from app.api.v1.exams import router as exams_router
# from app.api.v1.ai import router as ai_router

api_router = APIRouter(prefix="/api/v1")

# 只挂载已经写好的papers路由
api_router.include_router(papers_router)

# 其他路由也先注释掉
# api_router.include_router(auth_router)
# api_router.include_router(questions_router)
# api_router.include_router(exams_router)
# api_router.include_router(ai_router)
# 导出api_router，让main.py可以导入
__all__ = ["api_router"]