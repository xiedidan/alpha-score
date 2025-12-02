"""
系统日志模型
存储系统运行日志
"""
from sqlalchemy import String, Text, DateTime, Index, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from enum import Enum
from .database import Base


class LogLevel(str, Enum):
    """日志级别"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class SystemLog(Base):
    """
    系统日志表
    存储应用运行日志
    """

    __tablename__ = "system_logs"

    # 主键
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # 日志级别
    level: Mapped[str] = mapped_column(
        SQLEnum(LogLevel, values_callable=lambda x: [e.value for e in x]),
        default=LogLevel.INFO,
        nullable=False,
        index=True,
    )

    # 模块名称
    module: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    # 日志消息
    message: Mapped[str] = mapped_column(Text, nullable=False)

    # 额外数据（JSON 格式）
    extra_data: Mapped[str | None] = mapped_column(Text, nullable=True)

    # 创建时间
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )

    # 索引
    __table_args__ = (
        Index("idx_system_logs_level", "level"),
        Index("idx_system_logs_module", "module"),
        Index("idx_system_logs_created_at", "created_at"),
        Index("idx_system_logs_level_created", "level", "created_at"),
    )

    def __repr__(self) -> str:
        return (
            f"SystemLog(id={self.id}, level={self.level!r}, "
            f"module={self.module!r}, message={self.message[:50]!r})"
        )

    def to_dict(self) -> dict:
        """转换为字典"""
        import json
        extra_data = None
        if self.extra_data:
            try:
                extra_data = json.loads(self.extra_data)
            except json.JSONDecodeError:
                extra_data = self.extra_data

        return {
            "id": self.id,
            "level": self.level,
            "module": self.module,
            "message": self.message,
            "extra_data": extra_data,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
