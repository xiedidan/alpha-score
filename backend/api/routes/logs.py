"""
日志查询 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime, timedelta

from models.user import User
from api.dependencies import get_current_user
from loguru import logger

router = APIRouter(prefix="/api/logs", tags=["logs"])

# 日志根目录
LOG_DIR = Path(__file__).parent.parent.parent.parent / "logs"


@router.get("", response_model=Dict[str, Any])
async def query_logs(
    log_type: str = Query("app", description="日志类型: app, error, trade"),
    date: Optional[str] = Query(None, description="日志日期 (YYYY-MM-DD)"),
    level: Optional[str] = Query(None, description="日志级别: INFO, WARNING, ERROR"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    limit: int = Query(100, ge=1, le=1000, description="返回行数限制"),
    current_user: User = Depends(get_current_user)
):
    """
    查询日志
    
    需要登录认证
    """
    try:
        # 确定日志文件路径
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        log_file = LOG_DIR / log_type / f"{log_type}_{date}.log"
        
        if not log_file.exists():
            return {
                "code": 404,
                "message": f"Log file not found for {log_type} on {date}",
                "data": {
                    "logs": [],
                    "total": 0,
                    "log_type": log_type,
                    "date": date
                }
            }
        
        # 读取日志文件
        logs = []
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 过滤日志
        for line in lines[-limit * 10:]:  # 从最后往前读
            line = line.strip()
            if not line:
                continue
            
            # 级别过滤
            if level and level.upper() not in line:
                continue
            
            # 关键词过滤
            if keyword and keyword.lower() not in line.lower():
                continue
            
            logs.append(line)
            
            if len(logs) >= limit:
                break
        
        # 倒序（最新的在前）
        logs.reverse()
        
        return {
            "code": 200,
            "message": "Logs retrieved successfully",
            "data": {
                "logs": logs[:limit],
                "total": len(logs),
                "log_type": log_type,
                "date": date,
                "filters": {
                    "level": level,
                    "keyword": keyword
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to query logs: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to query logs: {str(e)}"
        )


@router.get("/files", response_model=Dict[str, Any])
async def list_log_files(
    log_type: str = Query("app", description="日志类型: app, error, trade"),
    current_user: User = Depends(get_current_user)
):
    """
    列出可用的日志文件
    
    需要登录认证
    """
    try:
        log_dir = LOG_DIR / log_type
        
        if not log_dir.exists():
            return {
                "code": 404,
                "message": f"Log directory not found for {log_type}",
                "data": {
                    "files": [],
                    "log_type": log_type
                }
            }
        
        # 获取所有日志文件
        files = []
        for file in sorted(log_dir.glob(f"{log_type}_*.log"), reverse=True):
            files.append({
                "name": file.name,
                "size": file.stat().st_size,
                "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
            })
        
        return {
            "code": 200,
            "message": "Log files listed successfully",
            "data": {
                "files": files,
                "log_type": log_type,
                "total": len(files)
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to list log files: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list log files: {str(e)}"
        )


@router.get("/stats", response_model=Dict[str, Any])
async def get_log_stats(
    current_user: User = Depends(get_current_user)
):
    """
    获取日志统计信息
    
    需要登录认证
    """
    try:
        stats = {}
        
        for log_type in ["app", "error", "trade"]:
            log_dir = LOG_DIR / log_type
            
            if log_dir.exists():
                files = list(log_dir.glob(f"{log_type}_*.log"))
                total_size = sum(f.stat().st_size for f in files)
                
                stats[log_type] = {
                    "file_count": len(files),
                    "total_size": total_size,
                    "total_size_mb": round(total_size / 1024 / 1024, 2),
                    "latest_file": files[0].name if files else None
                }
            else:
                stats[log_type] = {
                    "file_count": 0,
                    "total_size": 0,
                    "total_size_mb": 0,
                    "latest_file": None
                }
        
        return {
            "code": 200,
            "message": "Log statistics retrieved successfully",
            "data": stats
        }
        
    except Exception as e:
        logger.error(f"Failed to get log stats: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get log stats: {str(e)}"
        )
