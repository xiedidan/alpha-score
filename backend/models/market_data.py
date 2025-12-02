"""
市场数据模型
存储 OHLCV + ATR 数据
"""
from sqlalchemy import String, Integer, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from .database import Base


class MarketData(Base):
    """
    市场数据表
    存储 K 线数据（OHLCV）和 ATR 指标
    """

    __tablename__ = "market_data"

    # 主键
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # 交易对
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)

    # 时间戳
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)

    # 时间周期（1m, 5m, 15m, 1h, 4h, 1d）
    interval: Mapped[str] = mapped_column(String(10), nullable=False)

    # 开盘价（整数存储，单位：聪）
    open: Mapped[int] = mapped_column(Integer, nullable=False)

    # 最高价（整数存储，单位：聪）
    high: Mapped[int] = mapped_column(Integer, nullable=False)

    # 最低价（整数存储，单位：聪）
    low: Mapped[int] = mapped_column(Integer, nullable=False)

    # 收盘价（整数存储，单位：聪）
    close: Mapped[int] = mapped_column(Integer, nullable=False)

    # 成交量（整数存储，单位：聪）
    volume: Mapped[int] = mapped_column(Integer, nullable=False)

    # ATR 指标（整数存储，单位：聪）
    atr: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # 索引
    __table_args__ = (
        Index("idx_market_data_symbol", "symbol"),
        Index("idx_market_data_timestamp", "timestamp"),
        Index("idx_market_data_symbol_timestamp", "symbol", "timestamp"),
        Index("idx_market_data_symbol_interval_timestamp", "symbol", "interval", "timestamp"),
    )

    def __repr__(self) -> str:
        return (
            f"MarketData(id={self.id}, symbol={self.symbol!r}, "
            f"timestamp={self.timestamp}, close={self.close})"
        )

    @property
    def open_float(self) -> float:
        """获取浮点数形式的开盘价（BTC）"""
        return self.open / 100_000_000

    @property
    def high_float(self) -> float:
        """获取浮点数形式的最高价（BTC）"""
        return self.high / 100_000_000

    @property
    def low_float(self) -> float:
        """获取浮点数形式的最低价（BTC）"""
        return self.low / 100_000_000

    @property
    def close_float(self) -> float:
        """获取浮点数形式的收盘价（BTC）"""
        return self.close / 100_000_000

    @property
    def volume_float(self) -> float:
        """获取浮点数形式的成交量（BTC）"""
        return self.volume / 100_000_000

    @property
    def atr_float(self) -> float | None:
        """获取浮点数形式的 ATR（BTC）"""
        return self.atr / 100_000_000 if self.atr is not None else None

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "symbol": self.symbol,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "interval": self.interval,
            "open": self.open_float,
            "high": self.high_float,
            "low": self.low_float,
            "close": self.close_float,
            "volume": self.volume_float,
            "atr": self.atr_float,
        }
