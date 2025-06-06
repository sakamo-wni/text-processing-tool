"""
アプリケーション設定管理
"""

import os
from typing import Dict, Any, List
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field

class AppConfig(BaseModel):
    """アプリケーション設定クラス"""
    
    # API設定
    openai_api_key: str = Field(default="", description="OpenAI API Key")
    anthropic_api_key: str = Field(default="", description="Anthropic API Key")
    groq_api_key: str = Field(default="", description="Groq API Key")
    
    # モデル設定
    default_model: str = Field(default="gpt-3.5-turbo", description="デフォルトLLMモデル")
    available_models: Dict[str, List[str]] = Field(
        default={
            "openai": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
            "anthropic": ["claude-3-haiku", "claude-3-sonnet", "claude-3-opus"],
            "groq": ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"]
        },
        description="利用可能なモデル一覧"
    )
    
    # ファイル設定
    max_file_size_mb: int = Field(default=10, description="最大ファイルサイズ(MB)")
    supported_file_types: List[str] = Field(
        default=[".txt", ".pdf", ".docx", ".md"],
        description="サポートされるファイル形式"
    )
    
    # UI設定
    theme: str = Field(default="dark", description="UIテーマ")
    page_title: str = Field(default="Text Processing Tool", description="ページタイトル")
    page_icon: str = Field(default="🔍", description="ページアイコン")
    
    # 処理設定
    max_tokens: int = Field(default=4000, description="最大トークン数")
    temperature: float = Field(default=0.7, description="生成温度")
    
    def __init__(self, **data):
        """初期化時に環境変数を読み込み"""
        super().__init__(**data)
        self.load_from_env()
    
    def load_from_env(self):
        """環境変数から設定を読み込み"""
        # .envファイルを読み込み
        env_path = Path(__file__).parent.parent.parent / ".env"
        if env_path.exists():
            load_dotenv(env_path)
        
        # 環境変数から設定を更新
        self.openai_api_key = os.getenv("OPENAI_API_KEY", self.openai_api_key)
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", self.anthropic_api_key)
        self.groq_api_key = os.getenv("GROQ_API_KEY", self.groq_api_key)
        self.default_model = os.getenv("DEFAULT_MODEL", self.default_model)
        
        # その他の設定
        if os.getenv("MAX_FILE_SIZE_MB"):
            self.max_file_size_mb = int(os.getenv("MAX_FILE_SIZE_MB"))
        
        if os.getenv("SUPPORTED_FILE_TYPES"):
            self.supported_file_types = os.getenv("SUPPORTED_FILE_TYPES").split(",")
        
        self.theme = os.getenv("THEME", self.theme)
        self.page_title = os.getenv("PAGE_TITLE", self.page_title)
        self.page_icon = os.getenv("PAGE_ICON", self.page_icon)
    
    def get_provider_from_model(self, model_name: str) -> str:
        """モデル名からプロバイダーを取得"""
        for provider, models in self.available_models.items():
            if model_name in models:
                return provider
        return "openai"  # デフォルト
    
    def get_api_key_for_provider(self, provider: str) -> str:
        """プロバイダーに応じたAPIキーを取得"""
        key_mapping = {
            "openai": self.openai_api_key,
            "anthropic": self.anthropic_api_key,
            "groq": self.groq_api_key
        }
        return key_mapping.get(provider, "")
    
    def is_api_key_configured(self, provider: str) -> bool:
        """APIキーが設定されているかチェック"""
        api_key = self.get_api_key_for_provider(provider)
        return bool(api_key and api_key != "your_*_api_key_here")
    
    def get_configured_providers(self) -> List[str]:
        """設定済みのプロバイダー一覧を取得"""
        providers = []
        for provider in self.available_models.keys():
            if self.is_api_key_configured(provider):
                providers.append(provider)
        return providers
    
    def get_available_models_for_configured_providers(self) -> Dict[str, List[str]]:
        """設定済みプロバイダーの利用可能モデルを取得"""
        configured_providers = self.get_configured_providers()
        return {
            provider: models 
            for provider, models in self.available_models.items()
            if provider in configured_providers
        }
