"""
基础模型类
提供所有模型的通用字段和方法
"""
from datetime import datetime
from typing import Any, Dict
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    """时间戳混入类，提供创建时间和更新时间字段"""

    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        """创建时间"""
        return mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    @declared_attr
    def updated_at(cls) -> Mapped[datetime]:
        """更新时间"""
        return mapped_column(
            DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
            nullable=False,
        )


class BaseModel(TimestampMixin):
    """
    基础模型类，包含通用字段和方法
    所有业务模型都应继承此类
    """

    @declared_attr
    def id(cls) -> Column:
        """主键ID"""
        return Column(Integer, primary_key=True, autoincrement=True)

    def to_dict(self, exclude: list[str] | None = None) -> Dict[str, Any]:
        """
        将模型转换为字典

        Args:
            exclude: 要排除的字段列表

        Returns:
            模型字典表示
        """
        exclude = exclude or []
        result = {}
        for column in self.__table__.columns:
            if column.name not in exclude:
                value = getattr(self, column.name)
                # 处理特殊类型
                if isinstance(value, datetime):
                    result[column.name] = value.isoformat()
                else:
                    result[column.name] = value
        return result

    def __repr__(self) -> str:
        """字符串表示"""
        attrs = []
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            attrs.append(f"{column.name}={value!r}")
        return f"{self.__class__.__name__}({', '.join(attrs)})"
