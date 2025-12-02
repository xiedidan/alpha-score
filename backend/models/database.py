"""
数据库连接配置
使用 SQLAlchemy 2.0+ 异步 API + aiosqlite
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from pathlib import Path

# 数据库文件路径
DB_PATH = Path(__file__).parent.parent.parent / "data" / "alpha-score.db"
DB_URL = f"sqlite+aiosqlite:///{DB_PATH}"

# 创建异步引擎
engine = create_async_engine(
    DB_URL,
    echo=False,  # 设置为 True 可以看到 SQL 日志
    future=True,
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """所有模型的基类"""
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    获取数据库会话的依赖项
    用于 FastAPI 的 Depends

    使用示例:
        @app.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:
    """初始化数据库，创建所有表"""
    # 确保 data 目录存在
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    async with engine.begin() as conn:
        # 导入所有模型以确保它们被注册
        from . import user, config, trade, market_data, orderbook, points_history, grid_trade, system_log

        # 创建所有表
        await conn.run_sync(Base.metadata.create_all)


async def drop_db() -> None:
    """删除所有表（仅用于测试）"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
