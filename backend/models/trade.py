"""
交易记录模型
存储所有交易记录
"""
from sqlalchemy import String, Integer, DateTime, Index, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from enum import Enum
from .database import Base
from .base import TimestampMixin


class TradeSide(str, Enum):
    """交易方向"""
    BUY = "buy"
    SELL = "sell"


class TradeStatus(str, Enum):
    """交易状态"""
    PENDING = "pending"      # 待成交
    FILLED = "filled"        # 已成交
    CANCELLED = "cancelled"  # 已取消
    FAILED = "failed"        # 失败


class Trade(Base, TimestampMixin):
    """
    交易记录表
    存储所有买卖交易
    """

    __tablename__ = "trades"

    # 主键ID
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # 交易对
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)

    # 交易方向（buy/sell）
    side: Mapped[str] = mapped_column(
        SQLEnum(TradeSide, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
    )

    # 价格（使用整数存储，单位：聪 satoshi，1 BTC = 100,000,000 sats）
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    # 数量（使用整数存储，单位：聪 satoshi）
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    # 手续费（使用整数存储，单位：聪 satoshi）
    cost: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # 订单ID（交易所返回）
    order_id: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # 交易状态
    status: Mapped[str] = mapped_column(
        SQLEnum(TradeStatus, values_callable=lambda x: [e.value for e in x]),
        default=TradeStatus.PENDING,
        nullable=False,
    )

    # 备注
    note: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # 索引
    __table_args__ = (
        Index("idx_trades_symbol", "symbol"),
        Index("idx_trades_created_at", "created_at"),
        Index("idx_trades_symbol_created", "symbol", "created_at"),
    )

    def __repr__(self) -> str:
        return (
            f"Trade(id={self.id}, symbol={self.symbol!r}, "
            f"side={self.side!r}, price={self.price}, "
            f"quantity={self.quantity}, status={self.status!r})"
        )

    @property
    def price_float(self) -> float:
        """获取浮点数形式的价格（BTC）"""
        return self.price / 100_000_000

    @property
    def quantity_float(self) -> float:
        """获取浮点数形式的数量（BTC）"""
        return self.quantity / 100_000_000

    @property
    def cost_float(self) -> float:
        """获取浮点数形式的手续费（BTC）"""
        return self.cost / 100_000_000

    @property
    def total_value(self) -> int:
        """获取交易总价值（聪）"""
        return (self.price * self.quantity) // 100_000_000

    @property
    def total_value_float(self) -> float:
        """获取交易总价值（BTC）"""
        return self.total_value / 100_000_000
