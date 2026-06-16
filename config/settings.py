"""
アプリ全体の設定を一元管理するモジュール。

.env ファイルから環境変数を読み込み、settings オブジェクトとして公開する。
使い方: from config.settings import settings
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# プロジェクトルートにある .env を読み込む（既に読み込み済みでも上書きしない）
_env_path = Path(__file__).parent.parent / ".env"
load_dotenv(_env_path)


class Settings:
    """アプリ設定を保持するクラス。環境変数から値を取得する。"""

    app_name: str = "CareerSync AI"
    version: str = "0.1.0"

    @property
    def gemini_api_key(self) -> str:
        """Gemini APIキー。.env の GEMINI_API_KEY から取得する。"""
        key = os.getenv("GEMINI_API_KEY", "")
        if not key:
            raise ValueError(".env に GEMINI_API_KEY が設定されていません")
        return key

    @property
    def debug(self) -> bool:
        return os.getenv("DEBUG", "false").lower() == "true"


settings = Settings()
