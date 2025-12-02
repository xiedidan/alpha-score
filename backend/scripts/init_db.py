"""
数据库初始化脚本
创建所有表并插入初始数据
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import init_db, AsyncSessionLocal, User, Config
from sqlalchemy import select
from utils.security import hash_password


async def create_initial_data():
    """创建初始数据"""
    async with AsyncSessionLocal() as session:
        # 创建默认管理员用户
        result = await session.execute(
            select(User).where(User.username == "admin")
        )
        admin_exists = result.scalar_one_or_none()

        if not admin_exists:
            # 生成密码哈希
            password = "admin123"
            password_hash = hash_password(password)

            admin_user = User(
                username="admin",
                password_hash=password_hash,
                role="admin",
                is_active=True,
            )
            session.add(admin_user)
            print("✓ 创建默认管理员用户: admin / admin123")
        else:
            print("ℹ 管理员用户已存在，跳过创建")

        # 创建默认配置
        default_configs = [
            {
                "key": "trading.enabled",
                "value": "false",
                "description": "是否启用自动交易",
            },
            {
                "key": "trading.symbol",
                "value": '"BTC/USDT"',
                "description": "交易对",
            },
            {
                "key": "trading.max_position",
                "value": "100000000",  # 1 BTC in satoshi
                "description": "最大持仓量（聪）",
            },
            {
                "key": "grid.enabled",
                "value": "false",
                "description": "是否启用网格交易",
            },
            {
                "key": "grid.levels",
                "value": "10",
                "description": "网格层数",
            },
            {
                "key": "grid.range",
                "value": "0.05",
                "description": "网格范围（百分比）",
            },
            {
                "key": "points.base_per_day",
                "value": "100",
                "description": "每日基础积分",
            },
            {
                "key": "points.trade_multiplier",
                "value": "0.01",
                "description": "交易积分倍数",
            },
        ]

        for config_data in default_configs:
            # 检查配置是否存在
            result = await session.execute(
                select(Config).where(Config.key == config_data['key'])
            )
            config_exists = result.scalar_one_or_none()

            if not config_exists:
                config = Config(
                    key=config_data["key"],
                    value=config_data["value"],
                    description=config_data.get("description"),
                )
                session.add(config)
                print(f"✓ 创建配置: {config_data['key']}")
            else:
                print(f"ℹ 配置 {config_data['key']} 已存在，跳过创建")

        await session.commit()


async def main():
    """主函数"""
    print("=" * 60)
    print("Alpha-Score 数据库初始化")
    print("=" * 60)
    print()

    # 初始化数据库（创建所有表）
    print("正在创建数据库表...")
    try:
        await init_db()
        print("✓ 数据库表创建成功")
        print()
    except Exception as e:
        print(f"✗ 数据库表创建失败: {e}")
        return

    # 创建初始数据
    print("正在创建初始数据...")
    try:
        await create_initial_data()
        print()
        print("✓ 初始数据创建成功")
    except Exception as e:
        print(f"✗ 初始数据创建失败: {e}")
        import traceback
        traceback.print_exc()
        return

    print()
    print("=" * 60)
    print("数据库初始化完成！")
    print("=" * 60)
    print()
    print("默认管理员账户:")
    print("  用户名: admin")
    print("  密码: admin123")
    print()
    print("请及时修改默认密码！")


if __name__ == "__main__":
    asyncio.run(main())
