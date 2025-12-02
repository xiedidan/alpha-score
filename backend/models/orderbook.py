"""
盘口快照模型
存储订单簿快照数据
"""
from sqlalchemy import String, Text, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import json
from .database import Base


class OrderbookSnapshot(Base):
    """
    盘口快照表
    存储某一时刻的完整订单簿数据
    """

    __tablename__ = "orderbook_snapshots"

    # 主键
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # 交易对
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)

    # 时间戳
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)

    # 买单列表（JSON 格式存储）
    # 格式：[{"price": 50000.5, "quantity": 0.1}, ...]
    bids: Mapped[str] = mapped_column(Text, nullable=False)

    # 卖单列表（JSON 格式存储）
    # 格式：[{"price": 50100.5, "quantity": 0.1}, ...]
    asks: Mapped[str] = mapped_column(Text, nullable=False)

    # 索引
    __table_args__ = (
        Index("idx_orderbook_symbol", "symbol"),
        Index("idx_orderbook_timestamp", "timestamp"),
        Index("idx_orderbook_symbol_timestamp", "symbol", "timestamp"),
    )

    def __repr__(self) -> str:
        return (
            f"OrderbookSnapshot(id={self.id}, symbol={self.symbol!r}, "
            f"timestamp={self.timestamp})"
        )

    def get_bids(self) -> list[dict]:
        """获取解析后的买单列表"""
        try:
            return json.loads(self.bids)
        except json.JSONDecodeError:
            return []

    def set_bids(self, bids: list[dict]) -> None:
        """设置买单列表"""
        self.bids = json.dumps(bids, ensure_ascii=False)

    def get_asks(self) -> list[dict]:
        """获取解析后的卖单列表"""
        try:
            return json.loads(self.asks)
        except json.JSONDecodeError:
            return []

    def set_asks(self, asks: list[dict]) -> None:
        """设置卖单列表"""
        self.asks = json.dumps(asks, ensure_ascii=False)

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "symbol": self.symbol,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "bids": self.get_bids(),
            "asks": self.get_asks(),
        }

    @property
    def best_bid(self) -> float | None:
        """获取最高买价"""
        bids = self.get_bids()
        if bids and len(bids) > 0:
            return bids[0].get("price")
        return None

    @property
    def best_ask(self) -> float | None:
        """获取最低卖价"""
        asks = self.get_asks()
        if asks and len(asks) > 0:
            return asks[0].get("price")
        return None

    @property
    def spread(self) -> float | None:
        """获取买卖价差"""
        best_bid = self.best_bid
        best_ask = self.best_ask
        if best_bid is not None and best_ask is not None:
            return best_ask - best_bid
        return None
