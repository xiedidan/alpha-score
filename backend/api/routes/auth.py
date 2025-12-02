"""
认证路由
处理用户登录、登出、获取当前用户信息等
"""
from datetime import datetime, timezone
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from models.database import get_db
from models.user import User
from utils.security import verify_password
from utils.jwt import create_access_token, get_token_expire_time
from api.dependencies import get_current_user

# 创建路由器
router = APIRouter(prefix="/api/auth", tags=["Authentication"])


# === Pydantic 模型 ===

class LoginRequest(BaseModel):
    """登录请求模型"""
    username: str = Field(..., min_length=1, max_length=50, description="用户名")
    password: str = Field(..., min_length=1, description="密码")


class LoginResponse(BaseModel):
    """登录响应模型"""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token类型")
    expires_in: int = Field(..., description="Token过期时间（秒）")


class UserInfoResponse(BaseModel):
    """用户信息响应模型"""
    id: int
    username: str
    role: str
    is_active: bool
    last_login: str | None
    created_at: str
    updated_at: str


# === API 端点 ===

@router.post("/login", response_model=Dict[str, Any])
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    用户登录

    Args:
        request: 登录请求（用户名和密码）
        db: 数据库会话

    Returns:
        包含 access_token 的响应

    Raises:
        HTTPException: 用户名或密码错误时返回 401
    """
    # 查询用户
    result = await db.execute(
        select(User).where(User.username == request.username)
    )
    user = result.scalar_one_or_none()

    # 验证用户和密码
    if user is None or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 检查用户是否激活
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 生成 JWT token
    access_token = create_access_token(data={"sub": user.id})

    # 更新最后登录时间
    await db.execute(
        update(User)
        .where(User.id == user.id)
        .values(last_login=datetime.now(timezone.utc))
    )
    await db.commit()

    # 返回响应
    return {
        "code": 200,
        "message": "Login successful",
        "data": {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": get_token_expire_time()
        }
    }


@router.post("/logout", response_model=Dict[str, Any])
async def logout(
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    用户登出

    注意: 由于使用 JWT，服务端无法主动使 token 失效
    前端需要删除本地存储的 token

    Args:
        current_user: 当前登录用户

    Returns:
        登出成功消息
    """
    return {
        "code": 200,
        "message": "Logged out successfully",
        "data": {}
    }


@router.get("/me", response_model=Dict[str, Any])
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    获取当前登录用户信息

    Args:
        current_user: 当前登录用户

    Returns:
        用户信息
    """
    return {
        "code": 200,
        "message": "Success",
        "data": current_user.to_dict_safe()
    }
