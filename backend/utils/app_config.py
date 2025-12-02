"""
应用配置管理模块
负责加载、验证和管理应用配置
"""
import yaml
from pathlib import Path
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, validator
from loguru import logger
import threading


# ===== 配置数据模型 =====

class SystemConfig(BaseModel):
    """系统配置"""
    debug_port: int = 9222
    api_port: int = 8000
    log_level: str = "INFO"
    environment: str = "development"


class TradingConfig(BaseModel):
    """交易配置"""
    target_points_per_day: int = 5
    max_trade_count: int = 50
    min_order_value: float = 10.0
    max_order_value: float = 100.0
    price_deviation: float = 0.001
    check_interval: int = 60


class ATRConfig(BaseModel):
    """ATR风控配置"""
    enabled: bool = True
    period: int = 14
    multiplier: float = 1.5
    interval: int = 300


class PositionConfig(BaseModel):
    """仓位配置"""
    max_total_value: float = 500.0
    max_single_value: float = 100.0


class DailyLimitsConfig(BaseModel):
    """每日限额配置"""
    max_loss: float = 50.0
    max_volume: float = 5000.0


class RiskControlConfig(BaseModel):
    """风控配置"""
    atr: ATRConfig = Field(default_factory=ATRConfig)
    position: PositionConfig = Field(default_factory=PositionConfig)
    daily_limits: DailyLimitsConfig = Field(default_factory=DailyLimitsConfig)


class RandomDelayConfig(BaseModel):
    """随机延迟配置"""
    enabled: bool = True
    min: int = 1
    max: int = 5


class MouseSimulationConfig(BaseModel):
    """鼠标模拟配置"""
    enabled: bool = True
    speed: str = "medium"


class PageScrollConfig(BaseModel):
    """页面滚动配置"""
    enabled: bool = True
    probability: float = 0.3


class BehaviorConfig(BaseModel):
    """行为模拟配置"""
    random_delay: RandomDelayConfig = Field(default_factory=RandomDelayConfig)
    mouse_simulation: MouseSimulationConfig = Field(default_factory=MouseSimulationConfig)
    page_scroll: PageScrollConfig = Field(default_factory=PageScrollConfig)


class NotificationServiceConfig(BaseModel):
    """单个通知服务配置"""
    enabled: bool = False
    webhook: Optional[str] = None
    bot_token: Optional[str] = None
    chat_id: Optional[str] = None
    smtp_server: Optional[str] = None
    smtp_port: Optional[int] = None
    from_addr: Optional[str] = None
    to_addr: Optional[str] = None


class NotificationsConfig(BaseModel):
    """通知配置"""
    discord: NotificationServiceConfig = Field(default_factory=NotificationServiceConfig)
    telegram: NotificationServiceConfig = Field(default_factory=NotificationServiceConfig)
    email: NotificationServiceConfig = Field(default_factory=NotificationServiceConfig)


class DatabaseConfig(BaseModel):
    """数据库配置"""
    type: str = "sqlite"
    path: str = "data/alpha-score.db"
    echo: bool = False


class LoggingConfig(BaseModel):
    """日志配置"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    rotation: str = "daily"
    retention: int = 30
    max_size: int = 100


class LadderRange(BaseModel):
    """阶梯范围"""
    range: List[Optional[float]]
    points: float


class LaddersConfig(BaseModel):
    """阶梯配置"""
    balance_ladders: List[LadderRange] = Field(default_factory=list)
    volume_ladders: List[LadderRange] = Field(default_factory=list)


class SecretsConfig(BaseModel):
    """敏感配置"""
    api_keys: Dict[str, str] = Field(default_factory=dict)
    jwt: Dict[str, Any] = Field(default_factory=dict)
    notifications: Dict[str, str] = Field(default_factory=dict)
    email: Dict[str, str] = Field(default_factory=dict)


class AppConfig(BaseModel):
    """应用总配置"""
    system: SystemConfig = Field(default_factory=SystemConfig)
    trading: TradingConfig = Field(default_factory=TradingConfig)
    risk_control: RiskControlConfig = Field(default_factory=RiskControlConfig)
    behavior: BehaviorConfig = Field(default_factory=BehaviorConfig)
    notifications: NotificationsConfig = Field(default_factory=NotificationsConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    ladders: LaddersConfig = Field(default_factory=LaddersConfig)
    secrets: SecretsConfig = Field(default_factory=SecretsConfig)

    class Config:
        arbitrary_types_allowed = True


# ===== 配置管理器 =====

class ConfigManager:
    """配置管理器 - 单例模式"""
    
    _instance: Optional['ConfigManager'] = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._config: Optional[AppConfig] = None
            self._config_dir = Path(__file__).parent.parent.parent / "config"
            self._initialized = True
            self.load_config()
    
    def load_config(self) -> AppConfig:
        """加载所有配置文件"""
        try:
            # 加载主配置
            settings_path = self._config_dir / "settings.yaml"
            with open(settings_path, 'r', encoding='utf-8') as f:
                settings_data = yaml.safe_load(f) or {}
            
            # 加载阶梯配置
            ladders_path = self._config_dir / "ladders.yaml"
            if ladders_path.exists():
                with open(ladders_path, 'r', encoding='utf-8') as f:
                    ladders_data = yaml.safe_load(f) or {}
                settings_data['ladders'] = ladders_data
            
            # 加载敏感配置
            secrets_path = self._config_dir / "secrets.yaml"
            if secrets_path.exists():
                with open(secrets_path, 'r', encoding='utf-8') as f:
                    secrets_data = yaml.safe_load(f) or {}
                settings_data['secrets'] = secrets_data
            
            # 验证并创建配置对象
            self._config = AppConfig(**settings_data)
            logger.info("Configuration loaded successfully")
            return self._config
            
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            # 如果加载失败，使用默认配置
            self._config = AppConfig()
            return self._config
    
    def reload_config(self) -> AppConfig:
        """重新加载配置"""
        logger.info("Reloading configuration...")
        return self.load_config()
    
    def get_config(self) -> AppConfig:
        """获取当前配置"""
        if self._config is None:
            self.load_config()
        return self._config
    
    def update_config(self, config_dict: Dict[str, Any]) -> AppConfig:
        """更新配置（仅更新settings.yaml）"""
        try:
            settings_path = self._config_dir / "settings.yaml"
            
            # 读取现有配置
            with open(settings_path, 'r', encoding='utf-8') as f:
                current_data = yaml.safe_load(f) or {}
            
            # 深度合并配置
            def deep_merge(base: dict, update: dict) -> dict:
                for key, value in update.items():
                    if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                        base[key] = deep_merge(base[key], value)
                    else:
                        base[key] = value
                return base
            
            updated_data = deep_merge(current_data, config_dict)
            
            # 验证配置
            # 临时创建配置对象验证
            temp_config_data = updated_data.copy()
            if hasattr(self._config, 'ladders'):
                temp_config_data['ladders'] = self._config.ladders.dict()
            if hasattr(self._config, 'secrets'):
                temp_config_data['secrets'] = self._config.secrets.dict()
            
            AppConfig(**temp_config_data)  # 验证配置是否有效
            
            # 写入文件
            with open(settings_path, 'w', encoding='utf-8') as f:
                yaml.dump(updated_data, f, default_flow_style=False, allow_unicode=True)
            
            # 重新加载
            self.reload_config()
            logger.info("Configuration updated successfully")
            return self._config
            
        except Exception as e:
            logger.error(f"Failed to update configuration: {e}")
            raise
    
    def get_safe_config(self) -> Dict[str, Any]:
        """获取安全配置（移除敏感信息）"""
        config = self.get_config()
        config_dict = config.dict()
        
        # 移除敏感配置
        if 'secrets' in config_dict:
            config_dict.pop('secrets')
        
        # 移除通知配置中的敏感信息
        if 'notifications' in config_dict:
            for service in config_dict['notifications'].values():
                if isinstance(service, dict):
                    for key in ['webhook', 'bot_token', 'chat_id', 'smtp_password']:
                        if key in service and service[key]:
                            service[key] = "***"  # 脱敏
        
        return config_dict


# 全局配置管理器实例
config_manager = ConfigManager()


# ===== 便捷函数 =====

def get_config() -> AppConfig:
    """获取应用配置"""
    return config_manager.get_config()


def reload_config() -> AppConfig:
    """重新加载配置"""
    return config_manager.reload_config()


def get_safe_config() -> Dict[str, Any]:
    """获取安全配置（脱敏）"""
    return config_manager.get_safe_config()


def update_config(config_dict: Dict[str, Any]) -> AppConfig:
    """更新配置"""
    return config_manager.update_config(config_dict)
