"""
配置管理 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from pydantic import BaseModel

from models.user import User
from api.dependencies import get_current_user
from utils.app_config import get_config, reload_config, get_safe_config, update_config
from loguru import logger

router = APIRouter(prefix="/api/config", tags=["config"])


class ConfigUpdateRequest(BaseModel):
    """配置更新请求"""
    config: Dict[str, Any]


@router.get("", response_model=Dict[str, Any])
async def get_configuration(
    current_user: User = Depends(get_current_user)
):
    """
    获取当前配置（脱敏）
    
    需要登录认证
    """
    try:
        safe_config = get_safe_config()
        return {
            "code": 200,
            "message": "Configuration retrieved successfully",
            "data": safe_config
        }
    except Exception as e:
        logger.error(f"Failed to get configuration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve configuration"
        )


@router.put("", response_model=Dict[str, Any])
async def update_configuration(
    request: ConfigUpdateRequest,
    current_user: User = Depends(get_current_user)
):
    """
    更新配置
    
    需要登录认证
    只能更新 settings.yaml 中的配置
    """
    try:
        # 更新配置
        updated_config = update_config(request.config)
        
        # 返回更新后的安全配置
        safe_config = get_safe_config()
        
        return {
            "code": 200,
            "message": "Configuration updated successfully",
            "data": safe_config
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid configuration: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Failed to update configuration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update configuration"
        )


@router.post("/reload", response_model=Dict[str, Any])
async def reload_configuration(
    current_user: User = Depends(get_current_user)
):
    """
    手动重新加载配置
    
    需要登录认证
    """
    try:
        reload_config()
        safe_config = get_safe_config()
        
        return {
            "code": 200,
            "message": "Configuration reloaded successfully",
            "data": safe_config
        }
    except Exception as e:
        logger.error(f"Failed to reload configuration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reload configuration"
        )


@router.get("/schema", response_model=Dict[str, Any])
async def get_configuration_schema(
    current_user: User = Depends(get_current_user)
):
    """
    获取配置模式（用于前端表单生成）
    
    需要登录认证
    """
    try:
        from utils.app_config import AppConfig
        
        schema = AppConfig.schema()
        
        return {
            "code": 200,
            "message": "Configuration schema retrieved successfully",
            "data": schema
        }
    except Exception as e:
        logger.error(f"Failed to get configuration schema: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve configuration schema"
        )
