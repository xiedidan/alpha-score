"""
用户模型
存储系统用户信息
"""
from sqlalchemy import String, DateTime, Index, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from .database import Base
from .base import BaseModel, TimestampMixin


class User(Base, TimestampMixin):
    """
    用户表
    存储系统登录用户信息
    """

    __tablename__ = "users"

    # 主键ID
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # 用户名（唯一）
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)

    # 密码哈希（使用 bcrypt）
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # 最后登录时间
    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # 是否激活
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # 用户角色（admin, user）
    role: Mapped[str] = mapped_column(String(20), default="user", nullable=False)

    # 索引
    __table_args__ = (
        Index("idx_username", "username"),
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username!r}, role={self.role!r})"

    def to_dict_safe(self) -> dict:
        """
        安全的字典表示（不包含密码）
        """
        result = {}
        for column in self.__table__.columns:
            if column.name != "password_hash":
                value = getattr(self, column.name)
                # 处理特殊类型
                if isinstance(value, datetime):
                    result[column.name] = value.isoformat()
                else:
                    result[column.name] = value
        return result
