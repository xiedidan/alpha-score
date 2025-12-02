"""
网格交易模型
存储网格交易记录
"""
from sqlalchemy import String, Integer, DateTime, Index, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from enum import Enum
from .database import Base
from .base import TimestampMixin


class GridTradeSide(str, Enum):
    """网格交易方向"""
    BUY = "buy"
    SELL = "sell"


class GridTradeStatus(str, Enum):
    """网格交易状态"""
    PENDING = "pending"      # 待成交
    FILLED = "filled"        # 已成交
    CANCELLED = "cancelled"  # 已取消
    FAILED = "failed"        # 失败


class GridTrade(Base, TimestampMixin):
    """
    网格交易表
    存储网格策略的交易记录
    """

    __tablename__ = "grid_trades"

    # 主键ID
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # 网格ID（同一个网格策略共用一个ID）
    grid_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    # 交易对
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)

    # 交易方向（buy/sell）
    side: Mapped[str] = mapped_column(
        SQLEnum(GridTradeSide, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
    )

    # 价格（整数存储，单位：聪）
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    # 数量（整数存储，单位：聪）
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    # 网格层级
    grid_level: Mapped[int] = mapped_column(Integer, nullable=False)

    # 订单ID（交易所返回）
    order_id: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # 交易状态
    status: Mapped[str] = mapped_column(
        SQLEnum(GridTradeStatus, values_callable=lambda x: [e.value for e in x]),
        default=GridTradeStatus.PENDING,
        nullable=False,
    )

    # 关联的买入/卖出订单ID（用于成对交易）
    paired_order_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # 备注
    note: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # 索引
    __table_args__ = (
        Index("idx_grid_trades_grid_id", "grid_id"),
        Index("idx_grid_trades_symbol", "symbol"),
        Index("idx_grid_trades_created_at", "created_at"),
        Index("idx_grid_trades_grid_id_status", "grid_id", "status"),
    )

    def __repr__(self) -> str:
        return (
            f"GridTrade(id={self.id}, grid_id={self.grid_id!r}, "
            f"symbol={self.symbol!r}, side={self.side!r}, "
            f"price={self.price}, level={self.grid_level})"
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
    def total_value(self) -> int:
        """获取交易总价值（聪）"""
        return (self.price * self.quantity) // 100_000_000

    @property
    def total_value_float(self) -> float:
        """获取交易总价值（BTC）"""
        return self.total_value / 100_000_000
