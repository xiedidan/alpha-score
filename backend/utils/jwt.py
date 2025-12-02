"""
JWT token 生成和验证工具
使用 python-jose 库
"""
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from jose import JWTError, jwt

from .config import settings  # 保持使用旧config以保证兼容性


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    创建 JWT access token

    Args:
        data: 要编码到 token 中的数据 (通常包含 sub: user_id)
        expires_delta: token 过期时间，默认从配置读取

    Returns:
        编码后的 JWT token 字符串
    """
    to_encode = data.copy()

    # 确保 sub 是字符串类型（python-jose 要求）
    if "sub" in to_encode and not isinstance(to_encode["sub"], str):
        to_encode["sub"] = str(to_encode["sub"])

    # 设置过期时间
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    # 生成 JWT token
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    解码并验证 JWT token

    Args:
        token: JWT token 字符串

    Returns:
        解码后的 payload，如果 token 无效则返回 None
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


def get_token_expire_time() -> int:
    """
    获取 token 过期时间（秒）

    Returns:
        过期时间（秒）
    """
    return settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
