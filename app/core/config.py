from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 临时写死，测试通过后再改回，这是我自己的用户名密码.env
    DATABASE_URL: str = "mysql+pymysql://root:559926@localhost:3306/student_exam_system"
    SECRET_KEY: str = "your-secret-key-here-change-it-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    AI_SERVICE_BASE_URL: str = "https://localhost:8001/api/v1"
    REDIS_URL: str = "redis://localhost:6379/0"

settings = Settings()