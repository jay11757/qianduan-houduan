# 学生考试系统架构文档

## 项目概述

基于FastAPI构建的学生考试系统后端，采用现代化的技术栈，包括SQLAlchemy 2.0异步ORM、JWT认证、MySQL数据库等技术。

## 技术栈

| 组件 | 选型 | 版本要求 |
|------|------|----------|
| Web框架 | FastAPI | >=0.104.1 |
| 数据库驱动 | SQLAlchemy + aiomysql | SQLAlchemy>=2.0.23, aiomysql>=0.2.1 |
| 密码哈希 | passlib + bcrypt | bcrypt>=4.1.0 |
| JWT | python-jose | - |
| 数据校验 | Pydantic V2 | - |
| 配置管理 | pydantic-settings | >=2.1.0 |

## 项目结构

```
app/
├── main.py                 # FastAPI应用入口，注册中间件和路由
├── core/                   # 核心功能模块
│   ├── config.py           # 配置管理，使用pydantic-settings读取.env
│   ├── database.py         # SQLAlchemy异步引擎和会话工厂
│   ├── security.py         # 密码哈希(bcrypt)和JWT令牌管理
│   └── dependencies.py     # 依赖注入(get_current_user等)
├── models/                 # 数据库模型
│   ├── user.py             # 用户模型
│   ├── question.py         # 题目模型
│   ├── paper.py            # 试卷模型
│   └── exam_record.py      # 考试记录模型
├── schemas/                # Pydantic数据模式
│   ├── user.py             # 用户相关数据模式
│   └── token.py            # 令牌相关数据模式
├── crud/                   # 数据库操作函数
│   ├── user.py             # 用户CRUD操作
│   └── base.py             # 基础CRUD操作(待完善)
└── api/                    # API路由
    └── v1/                 # v1版本API
        ├── auth.py         # 认证相关接口(注册/登录)
        └── users.py        # 用户相关接口
```

## 核心功能模块

### 1. 数据库模块 (app/core/database.py)

- **异步引擎**: 使用`create_async_engine`创建异步数据库连接
- **连接池**: 配置`pool_pre_ping=True`防止连接失效
- **会话工厂**: `async_sessionmaker`提供异步数据库会话
- **生命周期管理**: 在应用启动时初始化数据库，在关闭时释放资源

### 2. 安全模块 (app/core/security.py)

- **密码哈希**: 使用bcrypt算法加密用户密码
- **JWT令牌**: 实现令牌生成和解码功能
- **过期控制**: 默认30分钟过期时间

### 3. 依赖注入 (app/core/dependencies.py)

- **认证依赖**: `get_current_user`从JWT令牌中提取当前用户
- **权限控制**: `get_current_superuser`检查管理员权限
- **数据库会话**: `get_db`提供数据库会话依赖

## 数据模型

### 1. 用户模型 (User)

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | int | 主键, 索引 | 用户唯一标识 |
| name | String(50) | 唯一, 索引, 非空 | 用户名 |
| phone | String(20) | 唯一, 索引, 非空 | 手机号 |
| hashed_password | String(255) | 非空 | 加密后的密码 |
| role | String(20) | 默认"user" | 用户角色 |
| created_at | DateTime | 服务器默认 | 创建时间 |

### 2. 题目模型 (Question)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| title | String(200) | 题目标题 |
| question_type | QuestionType(Enum) | 题目类型(单选、多选、判断、填空、简答、论述) |
| difficulty | DifficultyLevel(Enum) | 难度等级(简单、中等、困难) |
| content | JSON | 题目内容(题干、选项、答案等) |
| category | String(50) | 分类 |
| tags | JSON | 标签列表 |
| score | float | 分值 |
| is_active | Boolean | 是否启用 |

### 3. 试卷模型 (Paper)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| title | String(200) | 试卷名称 |
| description | String(500) | 试卷描述 |
| question_ids | JSON | 题目ID列表 |
| config | JSON | 试卷配置(组卷规则、考试设置) |
| total_score | float | 总分 |
| duration_minutes | int | 考试时长(分钟) |
| is_published | Boolean | 是否发布 |
| is_active | Boolean | 是否启用 |

### 4. 考试记录模型 (ExamRecord)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| user_id | int | 用户ID |
| paper_id | int | 试卷ID |
| status | String(20) | 考试状态(in_progress/submitted/graded) |
| answers | JSON | 答题记录 |
| result | JSON | 考试结果 |
| score | float | 得分 |
| started_at | DateTime | 开始时间 |
| submitted_at | DateTime | 提交时间 |

## API接口

### 1. 认证接口 (POST /api/v1/auth/)

#### 用户注册: POST /api/v1/auth/register

**请求体**:
```json
{
  "name": "用户名",
  "phone": "13800138000",
  "password": "password123",
  "role": "user"
}
```

**请求校验**:
- 手机号格式: `^1[3-9]\d{9}$`
- 密码要求: 必须包含字母和数字，长度至少6位

**响应**:
```json
{
  "id": 1,
  "name": "用户名",
  "phone": "13800138000",
  "role": "user",
  "created_at": "2023-01-01T00:00:00"
}
```

**错误处理**:
- 400: 用户名或手机号已存在
- 201: 注册成功

#### 用户登录: POST /api/v1/auth/login

**请求方式**: 表单提交 (OAuth2PasswordRequestForm)

**参数**:
- username: 用户名
- password: 密码

**响应**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**错误处理**:
- 401: 用户名或密码错误

### 2. 用户接口 (GET /api/v1/users/)

#### 获取当前用户信息: GET /api/v1/users/me

**请求头**: 
```
Authorization: Bearer <token>
```

**响应**:
```json
{
  "id": 1,
  "name": "用户名",
  "phone": "13800138000",
  "role": "user",
  "created_at": "2023-01-01T00:00:00"
}
```

**错误处理**:
- 401: 无效的认证凭证
- 403: 权限不足

## 认证机制

### JWT令牌流程

1. **用户登录**: 验证用户名和密码
2. **生成令牌**: 使用HS256算法生成JWT，payload包含用户ID
3. **返回令牌**: 客户端保存并用于后续请求
4. **验证令牌**: 每次请求通过`get_current_user`验证

### 令牌结构

```
Header: {"alg": "HS256", "typ": "JWT"}
Payload: {"sub": "user_id", "exp": "expiration_time"}
Signature: HMAC-SHA256(encoded_header + "." + encoded_payload, secret_key)
```

## 框架设计思路

### 1. 分层架构

- **API层**: 处理HTTP请求和响应
- **业务逻辑层**: 在API路由中实现
- **数据访问层**: CRUD模块
- **数据模型层**: SQLAlchemy模型
- **核心服务层**: 配置、安全、数据库连接等

### 2. 异步设计

- 全面采用异步编程模型
- 数据库操作全部异步化
- 提高并发处理能力

### 3. 安全设计

- 密码始终加密存储
- JWT令牌有过期时间
- 请求日志记录
- 输入数据严格校验

### 4. 可扩展性

- 模块化设计便于扩展
- JSON字段支持灵活的数据结构
- 权限系统支持角色管理

## 操作指南

### 1. 环境搭建

```bash
# 安装依赖
pip install -r requirements.txt

# 配置数据库连接
cp .env.example .env
# 编辑 .env 文件配置数据库连接信息
```

### 2. 启动应用

```bash
# 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 重置数据库

```bash
# 重置数据库(会删除所有数据，请谨慎操作)
python reset_db.py
```

### 4. 接口测试

```bash
# 运行认证系统测试
python test_auth.py
```

### 5. API文档

- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## 日志系统

- 应用启动/关闭日志
- 请求/响应日志
- 错误日志记录
- 身份验证日志

## 配置管理

通过`.env`文件管理配置：

- `DATABASE_URL`: 数据库连接字符串
- `SECRET_KEY`: JWT密钥
- `ALGORITHM`: JWT算法
- `ACCESS_TOKEN_EXPIRE_MINUTES`: 令牌过期时间

## 未来扩展方向

1. **题库管理**: 完善题目的增删改查接口
2. **试卷管理**: 实现试卷的创建、编辑、发布功能
3. **考试功能**: 实现在线考试、自动评分
4. **统计分析**: 考试成绩统计、学习分析
5. **权限管理**: 更细粒度的角色权限控制