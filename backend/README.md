# バックエンド API

## 概要

ドキュメント事前チェックツールのバックエンドAPIです。FastAPIを使用して実装されており、様々な形式のドキュメントから文書校正チェックを行います。

## 機能

- **ファイルアップロード**: Word、Excel、PDF、PowerPointファイルのアップロード
- **テキスト抽出**: textractを使用した多形式ドキュメントからのテキスト抽出
- **校正チェック**: 日本語文書の包括的な校正チェック
  - 二重助詞の検出
  - ゼロ幅スペースの検出
  - 表記ゆれの検出
  - 冗長表現の検出
  - 文体混在の検出
  - 長い文章の検出

## 開発環境のセットアップ

### 必要な環境

- Python 3.12+
- uv (Python パッケージマネージャー)

### インストール

1. 依存関係のインストール:
```bash
cd backend
uv sync
```

2. 開発サーバーの起動:
```bash
uv run python run_dev.py
```

または:

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker環境での実行

```bash
# プロジェクトルートから
docker-compose up --build
```

## API エンドポイント

### GET /
ヘルスチェック用エンドポイント

### GET /health
詳細なヘルスチェック情報

### GET /config
アプリケーション設定情報

### POST /check
ドキュメントの校正チェック

**リクエスト:**
- Content-Type: `multipart/form-data`
- Body: ファイル配列

**レスポンス:**
```json
{
  "total_files": 1,
  "processed_files": 1,
  "results": [
    {
      "filename": "document.docx",
      "status": "success",
      "text_length": 1000,
      "character_count": 1000,
      "line_count": 20,
      "word_count": 150,
      "issues": [
        {
          "type": "doubled_particle",
          "severity": "warning",
          "line": 5,
          "message": "助詞「が」が重複している可能性があります",
          "rule": "no-doubled-joshi",
          "suggestion": "文を分けるか、助詞を変更してください"
        }
      ]
    }
  ]
}
```

## テスト

APIのテストを実行:

```bash
# サーバーが起動していることを確認してから
uv run python test_api.py
```

## 設定

環境変数で以下の設定が可能:

- `MAX_FILE_SIZE`: 最大ファイルサイズ（バイト、デフォルト: 50MB）
- `MAX_FILES_COUNT`: 最大ファイル数（デフォルト: 10）
- `LOG_LEVEL`: ログレベル（デフォルト: INFO）
- `CORS_ORIGINS`: CORS許可オリジン（デフォルト: *）
- `TEMP_DIR`: 一時ファイル保存ディレクトリ（デフォルト: /tmp）

## 対応ファイル形式

- Word: `.docx`, `.doc`
- Excel: `.xlsx`, `.xls`
- PDF: `.pdf`
- PowerPoint: `.pptx`, `.ppt`

## ログ

アプリケーションはstructured loggingを使用しており、以下の情報をログに出力します:

- ファイルアップロード情報
- テキスト抽出結果
- 校正チェック結果
- エラー情報

## トラブルシューティング

### textractのエラー

textractでエラーが発生する場合、必要なシステム依存関係が不足している可能性があります。Dockerを使用することを推奨します。

### メモリ不足

大きなファイルを処理する際にメモリ不足が発生する場合は、`MAX_FILE_SIZE`を調整してください。

### 日本語テキストの文字化け

文字エンコーディングの問題が発生した場合、複数のエンコーディングで自動的に試行します。
