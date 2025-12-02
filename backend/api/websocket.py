"""
WebSocket连接管理器
用于实时推送交易数据、市场信息、系统状态等
"""
from typing import List, Dict, Any
from datetime import datetime
import json
import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from utils.logger import logger


class ConnectionManager:
    """WebSocket连接管理器"""

    def __init__(self):
        # 存储所有活跃连接
        self.active_connections: List[WebSocket] = []
        # 存储连接ID映射（可选，用于区分不同客户端）
        self.connection_ids: Dict[WebSocket, str] = {}
        # 心跳任务列表
        self.heartbeat_tasks: Dict[WebSocket, asyncio.Task] = {}

    async def connect(self, websocket: WebSocket, client_id: str = None):
        """
        接受新的WebSocket连接

        Args:
            websocket: WebSocket连接对象
            client_id: 客户端ID（可选）
        """
        await websocket.accept()
        self.active_connections.append(websocket)

        if client_id:
            self.connection_ids[websocket] = client_id

        logger.info(f"WebSocket连接建立: {client_id or 'anonymous'}, 当前连接数: {len(self.active_connections)}")

        # 启动心跳检测
        self.heartbeat_tasks[websocket] = asyncio.create_task(
            self._heartbeat(websocket)
        )

        # 发送欢迎消息
        await self.send_personal_message({
            "type": "connection_established",
            "data": {
                "client_id": client_id or "anonymous",
                "server_time": datetime.utcnow().isoformat() + "Z"
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }, websocket)

    def disconnect(self, websocket: WebSocket):
        """
        断开WebSocket连接

        Args:
            websocket: WebSocket连接对象
        """
        client_id = self.connection_ids.get(websocket, "unknown")

        # 取消心跳任务
        if websocket in self.heartbeat_tasks:
            self.heartbeat_tasks[websocket].cancel()
            del self.heartbeat_tasks[websocket]

        # 移除连接
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

        if websocket in self.connection_ids:
            del self.connection_ids[websocket]

        logger.info(f"WebSocket连接断开: {client_id}, 剩余连接数: {len(self.active_connections)}")

    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """
        发送消息给指定客户端

        Args:
            message: 消息内容（字典格式）
            websocket: 目标WebSocket连接
        """
        try:
            await websocket.send_text(json.dumps(message, ensure_ascii=False))
        except Exception as e:
            logger.error(f"发送消息失败: {e}")
            self.disconnect(websocket)

    async def broadcast(self, message: Dict[str, Any]):
        """
        广播消息给所有连接的客户端

        Args:
            message: 消息内容（字典格式）
        """
        if not self.active_connections:
            logger.debug("没有活跃连接，跳过广播")
            return

        logger.debug(f"广播消息给 {len(self.active_connections)} 个客户端: {message.get('type')}")

        # 记录断开的连接
        disconnected = []

        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message, ensure_ascii=False))
            except Exception as e:
                logger.warning(f"广播失败，标记断开连接: {e}")
                disconnected.append(connection)

        # 清理断开的连接
        for connection in disconnected:
            self.disconnect(connection)

    async def _heartbeat(self, websocket: WebSocket):
        """
        心跳检测任务

        Args:
            websocket: WebSocket连接对象
        """
        try:
            while True:
                await asyncio.sleep(30)  # 每30秒发送一次心跳

                try:
                    ping_message = {
                        "type": "ping",
                        "timestamp": datetime.utcnow().isoformat() + "Z"
                    }
                    await websocket.send_text(json.dumps(ping_message, ensure_ascii=False))
                    logger.debug("心跳ping发送成功")
                except Exception as e:
                    logger.warning(f"心跳ping发送失败: {e}")
                    self.disconnect(websocket)
                    break
        except asyncio.CancelledError:
            logger.debug("心跳任务已取消")

    def get_connection_count(self) -> int:
        """获取当前活跃连接数"""
        return len(self.active_connections)


# 全局连接管理器实例
manager = ConnectionManager()


# ============ 辅助函数：创建标准格式消息 ============

def create_message(msg_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    创建标准格式的WebSocket消息

    Args:
        msg_type: 消息类型
        data: 消息数据

    Returns:
        标准格式的消息字典
    """
    return {
        "type": msg_type,
        "data": data,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


def create_price_update(symbol: str, price: float, change_24h: float) -> Dict[str, Any]:
    """创建价格更新消息"""
    return create_message("price_update", {
        "symbol": symbol,
        "price": price,
        "change_24h": change_24h
    })


def create_orderbook_update(bids: List[List[float]], asks: List[List[float]]) -> Dict[str, Any]:
    """创建盘口更新消息"""
    return create_message("orderbook_update", {
        "bids": bids,
        "asks": asks
    })


def create_trade_executed(side: str, price: float, quantity: float, cost: float) -> Dict[str, Any]:
    """创建交易执行消息"""
    return create_message("trade_executed", {
        "side": side,
        "price": price,
        "quantity": quantity,
        "cost": cost
    })


def create_system_status(mode: str, points_today: float, volume_today: float) -> Dict[str, Any]:
    """创建系统状态消息"""
    return create_message("system_status", {
        "mode": mode,
        "points_today": points_today,
        "volume_today": volume_today
    })
