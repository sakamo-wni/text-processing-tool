"""
Text Processing Tool - Streamlit Application
高度なテキスト処理とLLM統合を行うアプリケーション
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import os

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from src.ui.components import (
    render_sidebar,
    render_main_content,
    setup_page_config
)
from src.core.config import AppConfig
from src.core.session_manager import SessionManager

def main():
    """メインアプリケーション"""
    
    # ページ設定
    setup_page_config()
    
    # 設定とセッション管理の初期化
    config = AppConfig()
    session_manager = SessionManager()
    
    # サイドバーの描画
    selected_page = render_sidebar()
    
    # メインコンテンツの描画
    render_main_content(selected_page, config, session_manager)

if __name__ == "__main__":
    main()
