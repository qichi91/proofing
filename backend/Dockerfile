# Python 3.12をベースイメージとして使用
FROM python:3.12-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムの依存関係をインストール
# textract用の依存関係も含む
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libxml2-dev \
    libxslt1-dev \
    antiword \
    unrtf \
    poppler-utils \
    tesseract-ocr \
    flac \
    ffmpeg \
    lame \
    libmad0 \
    libsox-fmt-mp3 \
    sox \
    libjpeg-dev \
    swig \
    libpulse-dev \
    ghostscript \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# uvを使用してPython依存関係を管理
COPY pyproject.toml uv.lock ./

# uvをインストール
RUN pip install uv

# 依存関係をインストール
RUN uv sync --frozen --no-dev

# アプリケーションコードをコピー
COPY app/ ./app/

# ポート8000を公開
EXPOSE 8000

# アプリケーションを起動
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]