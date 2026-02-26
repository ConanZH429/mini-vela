"""
脚手架抽象基类

定义所有脚手架必须实现的接口，用于：
- 配置 Docker 环境变量
- 生成容器初始化脚本
- 构建任务执行命令
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional


# 支持的模型列表（与 litellm_config.yaml 中的 model_name 对应）
SUPPORTED_MODELS = [
    # Anthropic Claude
    "claude-sonnet-4-5-20250929",
    "claude-opus-4-5-20251101",
    "claude-haiku-4-5-20251001",
    # Google Gemini
    "gemini-3-pro",
    # DeepSeek
    "deepseek-chat",
    # Zhipu GLM
    "glm-4.7",
]

# 默认模型
DEFAULT_MODEL = "claude-sonnet-4-5-20250929"


class BaseScaffold(ABC):
    """
    脚手架抽象基类
    
    """
    
    # 脚手架名称，用于匹配 case["scaffold"]["name"]
    name: str = ""
    
    @abstractmethod
    def get_docker_env(self, proxy_url: str, model: Optional[str] = None) -> Dict[str, str]:
        """
        返回 Docker 容器需要的环境变量
        
        Args:
            proxy_url: LiteLLM Proxy 的 URL，如 "http://host.docker.internal:4000"
            model: 可选的模型名称，用于某些需要在环境变量中指定模型的脚手架
        
        Returns:
            环境变量字典，如 {"ANTHROPIC_BASE_URL": "...", "ANTHROPIC_API_KEY": "..."}
        
        示例：
            - Claude Code: {"ANTHROPIC_BASE_URL": proxy_url, "ANTHROPIC_API_KEY": "fake-key"}
            - Kilo-Dev: {"KILO_API_URL": proxy_url, "KILO_API_KEY": "fake-key"}
        """
        pass
    
    @abstractmethod
    def get_setup_script(self, proxy_url: str, model: Optional[str] = None) -> str:
        """
        返回容器启动时的初始化脚本
        
        用于在容器内创建配置文件、设置环境等。
        
        Args:
            proxy_url: LiteLLM Proxy 的 URL
            model: 可选的模型名称，用于配置文件中指定模型
        
        Returns:
            Shell 脚本字符串，如 "mkdir -p ~/.claude && echo '...' > ~/.claude/settings.json"
        
        示例：
            - Claude Code: 创建 ~/.claude/settings.json，配置 API URL 和权限
            - Kilo-Dev: 可能创建 ~/.kilo/config.yaml
        """
        pass
    
    @abstractmethod
    def build_commands(
        self, 
        queries: List[str], 
        system_prompt: Optional[str] = None,
        model: Optional[str] = None
    ) -> List[str]:
        """
        根据用户查询列表构建任务命令序列
        
        Args:
            queries: 用户查询列表，如 ["第一个问题", "追问"]
            system_prompt: 可选的系统提示词
            model: 可选的模型名称，用于命令行参数中指定模型
        
        Returns:
            命令列表，如 ["claude -p '问题1'", "claude -c -p '问题2'"]
        
        说明：
            - 第一个查询通常需要初始化会话
            - 后续查询通常使用 "continue" 模式
            - 不同脚手架的命令格式可能完全不同
        """
        pass
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name='{self.name}'>"

