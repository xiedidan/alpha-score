"""
Alpha-Score Backend API
FastAPI应用主入口
"""
from datetime import datetime
from typing import Any, Dict
import time

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# 导入路由
from api.routes import auth_router
from api.routes.config import router as config_router
from api.routes.logs import router as logs_router
from api.routes.trades import router as trades_router

# 配置日志 - 使用新的日志模块
from utils.logger import logger, setup_logger

# 初始化日志系统
setup_logger(log_level="INFO")

# 创建FastAPI应用实例
app = FastAPI(
    title="Alpha-Score API",
    description="Alpha量化交易策略管理系统后端API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ============ 中间件配置 ============

# 1. CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vue3开发服务器
        "http://127.0.0.1:5173",
        "http://localhost:5174",  # Vue3备用端口
        "http://127.0.0.1:5174",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 2. 请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """记录所有HTTP请求"""
    start_time = time.time()

    # 记录请求信息
    logger.info(f"→ {request.method} {request.url.path}")

    # 处理请求
    response = await call_next(request)

    # 计算处理时间
    process_time = time.time() - start_time

    # 记录响应信息
    logger.info(f"← {request.method} {request.url.path} - {response.status_code} ({process_time:.3f}s)")

    # 添加处理时间到响应头
    response.headers["X-Process-Time"] = str(process_time)

    return response


# ============ 异常处理器 ============

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """处理请求验证错误"""
    logger.warning(f"Validation error on {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "code": 422,
            "message": "Request validation failed",
            "data": {
                "errors": exc.errors(),
                "body": exc.body
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    logger.error(f"Unhandled exception on {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "Internal server error",
            "data": {
                "error": str(exc),
                "path": request.url.path
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )


# ============ 注册路由 ============

app.include_router(auth_router)
app.include_router(config_router)
app.include_router(logs_router)
app.include_router(trades_router)


# ============ 工具函数 ============

def create_response(
    code: int = 200,
    message: str = "Success",
    data: Any = None
) -> Dict[str, Any]:
    """
    创建统一格式的API响应

    Args:
        code: 状态码
        message: 响应消息
        data: 响应数据

    Returns:
        标准格式的响应字典
    """
    return {
        "code": code,
        "message": message,
        "data": data if data is not None else {},
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


# ============ 基础路由 ============

@app.get("/", tags=["Root"])
async def root() -> Dict[str, Any]:
    """
    根路径 - 欢迎信息

    Returns:
        欢迎消息
    """
    logger.info("Root endpoint accessed")
    return create_response(
        message="Welcome to Alpha-Score API",
        data={
            "service": "Alpha-Score Backend",
            "version": "1.0.0",
            "status": "running",
            "apis": {
                "auth": "/api/auth/*",
                "config": "/api/config/*",
                "logs": "/api/logs/*",
                "trades": "/api/trades/*"
            }
        }
    )


@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, Any]:
    """
    健康检查端点

    Returns:
        服务健康状态
    """
    logger.debug("Health check endpoint accessed")
    return create_response(
        message="Service is healthy",
        data={
            "status": "healthy",
            "service": "alpha-score-backend",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )


@app.get("/api", tags=["API Info"])
async def api_info() -> Dict[str, Any]:
    """
    API信息端点

    Returns:
        API概览信息
    """
    return create_response(
        message="API Information",
        data={
            "version": "1.0.0",
            "endpoints": {
                "auth": {
                    "prefix": "/api/auth",
                    "description": "用户认证相关接口",
                    "routes": ["POST /login", "GET /me", "POST /logout"]
                },
                "config": {
                    "prefix": "/api/config",
                    "description": "配置管理相关接口",
                    "routes": ["GET /", "PUT /", "POST /reload", "GET /schema"]
                },
                "logs": {
                    "prefix": "/api/logs",
                    "description": "日志查询相关接口",
                    "routes": ["GET /", "GET /files", "GET /stats"]
                },
                "trades": {
                    "prefix": "/api/trades",
                    "description": "交易相关接口",
                    "routes": ["GET /stats", "GET /history", "GET /status", "GET /market", "GET /funds", "GET /points"]
                }
            },
            "documentation": {
                "swagger": "/docs",
                "redoc": "/redoc"
            }
        }
    )


# ============ 生命周期事件 ============

@app.on_event("startup")
async def startup_event():
    """应用启动时的事件处理"""
    logger.info("=" * 60)
    logger.info("Alpha-Score Backend API is starting...")
    logger.info("API Routes registered:")
    logger.info("  - /api/auth/*    (Authentication)")
    logger.info("  - /api/config/*  (Configuration)")
    logger.info("  - /api/logs/*    (Logs)")
    logger.info("  - /api/trades/*  (Trading)")
    logger.info("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的事件处理"""
    logger.info("=" * 60)
    logger.info("Alpha-Score Backend API is shutting down...")
    logger.info("=" * 60)


# ============ 启动服务 ============

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting development server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
