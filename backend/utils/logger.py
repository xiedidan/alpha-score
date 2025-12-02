"""
统一日志管理模块
使用 Loguru 实现结构化日志
"""
from loguru import logger
from pathlib import Path
import sys
from typing import Optional

# 日志根目录
LOG_DIR = Path(__file__).parent.parent.parent / "logs"

# 日志格式
LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}"


def setup_logger(log_level: str = "INFO"):
    """
    配置Loguru日志系统
    
    Args:
        log_level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # 移除默认处理器
    logger.remove()
    
    # 1. 控制台输出 (开发环境)
    logger.add(
        sys.stderr,
        level=log_level,
        format=LOG_FORMAT,
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    
    # 2. 应用日志文件 (INFO及以上)
    logger.add(
        LOG_DIR / "app" / "app_{time:YYYY-MM-DD}.log",
        level="INFO",
        format=LOG_FORMAT,
        rotation="00:00",  # 每天午夜轮转
        retention="30 days",  # 保留30天
        compression="zip",  # 压缩旧日志
        encoding="utf-8",
        backtrace=True,
        diagnose=True
    )
    
    # 3. 错误日志文件 (ERROR及以上)
    logger.add(
        LOG_DIR / "error" / "error_{time:YYYY-MM-DD}.log",
        level="ERROR",
        format=LOG_FORMAT,
        rotation="00:00",
        retention="60 days",  # 错误日志保留更久
        compression="zip",
        encoding="utf-8",
        backtrace=True,
        diagnose=True
    )
    
    # 4. 交易日志文件 (专用于交易相关日志)
    logger.add(
        LOG_DIR / "trade" / "trade_{time:YYYY-MM-DD}.log",
        level="INFO",
        format=LOG_FORMAT,
        rotation="00:00",
        retention="90 days",  # 交易日志保留90天
        compression="zip",
        encoding="utf-8",
        filter=lambda record: "trade" in record["extra"].get("context", "").lower()
    )
    
    logger.info(f"Logger initialized with level: {log_level}")
    logger.info(f"Log directory: {LOG_DIR}")
    return logger


def get_logger(name: str):
    """
    获取logger实例
    
    Args:
        name: logger名称
    
    Returns:
        logger实例
    """
    return logger.bind(name=name)


def get_trade_logger():
    """
    获取交易专用logger
    
    Returns:
        交易logger实例
    """
    return logger.bind(context="trade")


# 默认初始化
setup_logger()

# 导出logger实例
__all__ = ["logger", "setup_logger", "get_logger", "get_trade_logger"]
