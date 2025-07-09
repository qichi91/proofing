"""
アプリケーション設定モジュール
"""
import os
from typing import List


class Settings:
    """アプリケーション設定クラス"""
    
    # ファイルサイズ制限（バイト）
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", 200 * 1024 * 1024))  # 50MB
    
    # 最大ファイル数
    MAX_FILES_COUNT: int = int(os.getenv("MAX_FILES_COUNT", 100))
    
    # 一時ファイル保存ディレクトリ
    TEMP_DIR: str = os.getenv("TEMP_DIR", "/tmp")
    
    # サポートされているファイル拡張子
    SUPPORTED_EXTENSIONS: List[str] = [
        '.docx',              # Word (新形式のみ)
        '.xlsx',              # Excel (新形式のみ)
        '.pdf',               # PDF
        '.pptx'               # PowerPoint (新形式のみ)
    ]
    
    # CORS設定
    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # 校正チェック設定
    MAX_SENTENCE_LENGTH: int = int(os.getenv("MAX_SENTENCE_LENGTH", 120))
    
    # ログレベル
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # APIのタイトルと説明
    API_TITLE: str = "ドキュメント事前チェックツール API"
    API_DESCRIPTION: str = "ドキュメントの誤字脱字や表記ゆれをチェックするツール"
    API_VERSION: str = "1.0.0"


# シングルトンインスタンス
settings = Settings()
