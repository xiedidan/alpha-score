"""
积分历史模型
存储每日积分数据
"""
from sqlalchemy import Date, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from .database import Base


class PointsHistory(Base):
    """
    积分历史表
    存储每日积分计算结果
    """

    __tablename__ = "points_history"

    # 主键
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # 日期（唯一）
    date: Mapped[date] = mapped_column(Date, unique=True, nullable=False, index=True)

    # 基础积分
    base_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # 交易积分
    trade_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # 总积分
    total_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # 账户余额（整数存储，单位：聪）
    balance: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # 交易量（整数存储，单位：聪）
    volume: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # 交易次数
    trade_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # 备注
    note: Mapped[str | None] = mapped_column(nullable=True)

    # 索引
    __table_args__ = (
        Index("idx_points_date", "date"),
    )

    def __repr__(self) -> str:
        return (
            f"PointsHistory(id={self.id}, date={self.date}, "
            f"total_points={self.total_points}, balance={self.balance})"
        )

    @property
    def balance_float(self) -> float:
        """获取浮点数形式的余额（BTC）"""
        return self.balance / 100_000_000

    @property
    def volume_float(self) -> float:
        """获取浮点数形式的交易量（BTC）"""
        return self.volume / 100_000_000

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "date": self.date.isoformat() if self.date else None,
            "base_points": self.base_points,
            "trade_points": self.trade_points,
            "total_points": self.total_points,
            "balance": self.balance_float,
            "volume": self.volume_float,
            "trade_count": self.trade_count,
            "note": self.note,
        }
