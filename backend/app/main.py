import os
import tempfile
import traceback
from typing import List
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# import textract

from .proofreading_rules import ProofreadingRules
from .text_extractor import TextExtractor
from .utils import FileHandler, format_file_size, logger
from .config import settings


app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION
)

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CheckResult(BaseModel):
    filename: str
    status: str
    text_length: int
    character_count: int
    line_count: int
    word_count: int
    issues: List[dict]
    error_message: str = None


class CheckResponse(BaseModel):
    total_files: int
    processed_files: int
    results: List[CheckResult]


@app.get("/")
async def root():
    """ヘルスチェック用エンドポイント"""
    return {
        "message": settings.API_TITLE, 
        "status": "running",
        "version": settings.API_VERSION
    }


@app.get("/health")
async def health_check():
    """詳細ヘルスチェック"""
    return {
        "status": "healthy",
        "version": settings.API_VERSION,
        "supported_extensions": settings.SUPPORTED_EXTENSIONS,
        "max_file_size": format_file_size(settings.MAX_FILE_SIZE),
        "max_files_count": settings.MAX_FILES_COUNT
    }


@app.get("/config")
async def get_config():
    """設定情報を取得"""
    return {
        "max_file_size": settings.MAX_FILE_SIZE,
        "max_files_count": settings.MAX_FILES_COUNT,
        "supported_extensions": settings.SUPPORTED_EXTENSIONS,
        "max_sentence_length": settings.MAX_SENTENCE_LENGTH
    }


@app.post("/check", response_model=CheckResponse)
async def check_documents(files: List[UploadFile] = File(...)):
    """
    ドキュメントをアップロードして校正チェックを実行する
    """
    logger.info(f"チェック開始: {len(files)}ファイル")
    
    # ファイルのバリデーション
    try:
        FileHandler.validate_files(files)
    except HTTPException as e:
        logger.error(f"ファイルバリデーションエラー: {e.detail}")
        raise e
    
    results = []
    temp_files = []
    
    try:
        for file in files:
            temp_file = None
            try:
                logger.info(f"ファイル処理開始: {file.filename}")
                
                # 一時ファイルに保存
                temp_file = FileHandler.save_temp_file(file)
                temp_files.append(temp_file)
                
                # テキスト抽出
                extracted_text = TextExtractor.extract_text(temp_file)
                cleaned_text = TextExtractor.clean_extracted_text(extracted_text)
                text_stats = TextExtractor.get_text_stats(cleaned_text)
                
                # 校正チェック実行
                issues = perform_proofreading_check(cleaned_text)
                
                logger.info(f"ファイル処理完了: {file.filename}, 問題数: {len(issues)}")
                
                results.append(CheckResult(
                    filename=file.filename,
                    status="success",
                    text_length=len(cleaned_text),
                    character_count=text_stats['character_count'],
                    line_count=text_stats['line_count'],
                    word_count=text_stats['word_count'],
                    issues=issues
                ))
                
            except Exception as e:
                logger.error(f"ファイル処理エラー: {file.filename}, エラー: {e}")
                results.append(CheckResult(
                    filename=file.filename,
                    status="error",
                    text_length=0,
                    character_count=0,
                    line_count=0,
                    word_count=0,
                    issues=[],
                    error_message=f"処理中にエラーが発生しました: {str(e)}"
                ))
    
    finally:
        # 一時ファイルのクリーンアップ
        FileHandler.cleanup_temp_files(temp_files)
    
    successful_files = len([r for r in results if r.status == "success"])
    logger.info(f"チェック完了: {successful_files}/{len(files)}ファイル成功")
    
    return CheckResponse(
        total_files=len(files),
        processed_files=successful_files,
        results=results
    )

# 校正ルール取得API
@app.get("/rules")
async def get_rules():
    rules_path = os.path.join(os.path.dirname(__file__), "rules.json")
    try:
        with open(rules_path, encoding="utf-8") as f:
            rules = f.read()
        return JSONResponse(content=rules, media_type="application/json")
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# 校正ルール更新API
@app.post("/rules")
async def update_rules(request: Request):
    rules_path = os.path.join(os.path.dirname(__file__), "rules.json")
    try:
        rules_json = await request.json()
        # バリデーション: 配列であること
        if not isinstance(rules_json, list):
            return JSONResponse(content={"error": "ルールは配列形式で送信してください"}, status_code=400)
        # 書き込み
        with open(rules_path, "w", encoding="utf-8") as f:
            import json
            json.dump(rules_json, f, ensure_ascii=False, indent=2)
        # ルールを即時反映（ProofreadingRulesインスタンスを再生成）
        ProofreadingRules().load_external_rules()
        return {"message": "ルールを更新しました"}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

def perform_proofreading_check(text: str) -> List[dict]:
    """
    校正チェックを実行する
    ProofreadingRulesクラスを使用して包括的なチェックを行う
    """
    proofreading_rules = ProofreadingRules()
    return proofreading_rules.check_all_rules(text)


def is_supported_file(filename: str) -> bool:
    """サポートされているファイル形式かチェック（後方互換性のため残す）"""
    return FileHandler.is_supported_file(filename)


def save_temp_file(upload_file: UploadFile) -> str:
    """アップロードファイルを一時ファイルとして保存（後方互換性のため残す）"""
    return FileHandler.save_temp_file(upload_file)


def extract_text_from_file(file_path: str) -> str:
    """textractを使用してファイルからテキストを抽出（後方互換性のため残す）"""
    return TextExtractor.extract_text(file_path)


def cleanup_temp_files(temp_files: List[str]):
    """一時ファイルを削除（後方互換性のため残す）"""
    FileHandler.cleanup_temp_files(temp_files)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
