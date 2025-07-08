"""
ユーティリティ関数モジュール
"""
import logging
import os
import tempfile
from typing import List
from pathlib import Path

from fastapi import UploadFile, HTTPException

from .config import settings


# ロガーの設定
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
logger = logging.getLogger(__name__)


class FileHandler:
    """ファイル処理用ユーティリティクラス"""
    
    @staticmethod
    def validate_file(file: UploadFile) -> None:
        """ファイルのバリデーション"""
        # ファイル名のチェック
        if not file.filename:
            raise HTTPException(status_code=400, detail="ファイル名が指定されていません")
        
        # ファイル形式のチェック
        if not FileHandler.is_supported_file(file.filename):
            raise HTTPException(
                status_code=400, 
                detail=f"サポートされていないファイル形式です: {file.filename}"
            )
        
        # ファイルサイズのチェック（content-lengthがある場合）
        if hasattr(file, 'size') and file.size and file.size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400, 
                detail=f"ファイルサイズが上限を超えています: {file.size} bytes"
            )
    
    @staticmethod
    def validate_files(files: List[UploadFile]) -> None:
        """複数ファイルのバリデーション"""
        if len(files) > settings.MAX_FILES_COUNT:
            raise HTTPException(
                status_code=400, 
                detail=f"ファイル数が上限を超えています。最大 {settings.MAX_FILES_COUNT} ファイルまで"
            )
        
        for file in files:
            FileHandler.validate_file(file)
    
    @staticmethod
    def is_supported_file(filename: str) -> bool:
        """サポートされているファイル形式かチェック"""
        if not filename:
            return False
        
        return Path(filename).suffix.lower() in settings.SUPPORTED_EXTENSIONS
    
    @staticmethod
    def save_temp_file(upload_file: UploadFile) -> str:
        """アップロードファイルを一時ファイルとして保存"""
        try:
            suffix = Path(upload_file.filename).suffix
            with tempfile.NamedTemporaryFile(
                delete=False, 
                suffix=suffix,
                dir=settings.TEMP_DIR
            ) as temp_file:
                content = upload_file.file.read()
                
                # ファイルサイズのチェック（実際のサイズ）
                if len(content) > settings.MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"ファイルサイズが上限を超えています: {len(content)} bytes"
                    )
                
                temp_file.write(content)
                logger.info(f"一時ファイルを保存しました: {temp_file.name}")
                return temp_file.name
                
        except Exception as e:
            logger.error(f"一時ファイルの保存に失敗しました: {e}")
            raise HTTPException(status_code=500, detail="ファイルの保存に失敗しました")
    
    @staticmethod
    def cleanup_temp_files(temp_files: List[str]) -> None:
        """一時ファイルを削除"""
        for temp_file in temp_files:
            try:
                if temp_file and os.path.exists(temp_file):
                    os.unlink(temp_file)
                    logger.info(f"一時ファイルを削除しました: {temp_file}")
            except Exception as e:
                logger.error(f"一時ファイルの削除に失敗しました: {temp_file}, エラー: {e}")


def format_file_size(size_bytes: int) -> str:
    """ファイルサイズを人間が読みやすい形式にフォーマット"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"


def sanitize_filename(filename: str) -> str:
    """ファイル名をサニタイズ"""
    # 危険な文字を削除
    dangerous_chars = ['<', '>', ':', '"', '|', '?', '*', '\\', '/']
    for char in dangerous_chars:
        filename = filename.replace(char, '_')
    
    return filename
