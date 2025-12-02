"""
配置模型
KV 存储系统配置
"""
from sqlalchemy import String, Text, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import json
from .database import Base


class Config(Base):
    """
    配置表
    使用 KV 存储模式
    """

    __tablename__ = "config"

    # 主键
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # 配置键（唯一）
    key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)

    # 配置值（JSON 格式）
    value: Mapped[str] = mapped_column(Text, nullable=False)

    # 配置描述
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # 更新时间
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # 索引
    __table_args__ = (
        Index("idx_config_key", "key"),
    )

    def __repr__(self) -> str:
        return f"Config(key={self.key!r}, value={self.value!r})"

    def get_value(self) -> dict | list | str | int | float | bool | None:
        """获取解析后的配置值"""
        try:
            return json.loads(self.value)
        except json.JSONDecodeError:
            return self.value

    def set_value(self, value: dict | list | str | int | float | bool | None) -> None:
        """设置配置值（自动序列化为 JSON）"""
        if isinstance(value, (dict, list)):
            self.value = json.dumps(value, ensure_ascii=False)
        else:
            self.value = json.dumps(value)

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "key": self.key,
            "value": self.get_value(),
            "description": self.description,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
