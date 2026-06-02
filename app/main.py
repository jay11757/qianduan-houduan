from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 导入app/api/v1/__init__.py里定义的api_router
from app.api.v1 import api_router

# 创建FastAPI实例，添加标题和描述，方便看文档
app = FastAPI(
    title="在线考试系统API",
    description="试卷管理、题目管理、考试管理后端接口",
    version="1.0.0"
)

# 配置CORS跨域（前端调用必须加这个，否则浏览器会报错）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境允许所有来源，生产环境改成你的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载所有API路由
app.include_router(api_router)

# 根路径（用来测试服务是否正常启动）
@app.get("/", summary="根路径")
async def root():
    return {
        "message": "在线考试系统API服务已启动",
        "docs": "访问 /docs 查看接口文档",
        "version": "1.0.0"
    }

from app.core.database import engine
from app.models import paper, question, user

# 创建所有数据库表
paper.Base.metadata.create_all(bind=engine)
question.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)