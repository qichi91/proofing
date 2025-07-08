#!/usr/bin/env python3
"""
開発用サーバー起動スクリプト
"""
import uvicorn
from app.main import app

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 開発時のホットリロード
        log_level="info"
    )
