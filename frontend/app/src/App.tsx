import { useState, useEffect } from 'react';
import { FileUploader } from './components/FileUploader';
import CheckResults from './components/CheckResults';
import { api } from './api/client';
import type { CheckResponse, ConfigResponse } from './types/api';
import './App.css';

interface AppState {
  config: ConfigResponse | null;
  isLoading: boolean;
  isChecking: boolean;
  checkResults: CheckResponse | null;
  error: string | null;
  selectedFiles: File[];
}

function App() {
  const [state, setState] = useState<AppState>({
    config: null,
    isLoading: true,
    isChecking: false,
    checkResults: null,
    error: null,
    selectedFiles: [],
  });

  // アプリケーション初期化時に設定を取得
  useEffect(() => {
    const initializeApp = async () => {
      try {
        const config = await api.config();
        setState(prev => ({ ...prev, config, isLoading: false }));
      } catch (error) {
        console.error('Failed to load config:', error);
        setState(prev => ({
          ...prev,
          error: '設定の読み込みに失敗しました。バックエンドサーバーが起動していることを確認してください。',
          isLoading: false
        }));
      }
    };

    initializeApp();
  }, []);

  const handleFilesSelected = async (files: File[]) => {
    setState(prev => ({ ...prev, selectedFiles: files }));

    if (files.length === 0) {
      setState(prev => ({ ...prev, checkResults: null }));
      return;
    }

    setState(prev => ({ ...prev, isChecking: true, error: null, checkResults: null }));

    try {
      const results = await api.checkFiles(files);
      setState(prev => ({ ...prev, checkResults: results, isChecking: false }));
    } catch (error) {
      console.error('Failed to check documents:', error);
      setState(prev => ({
        ...prev,
        error: 'ドキュメントのチェックに失敗しました。ファイル形式やサイズを確認してください。',
        isChecking: false
      }));
    }
  };

  const resetResults = () => {
    setState(prev => ({ ...prev, checkResults: null, error: null, selectedFiles: [] }));
  };

  if (state.isLoading) {
    return (
      <div className="app">
        <div className="loading-message">
          <p>アプリケーションを初期化中...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>📄 ドキュメント事前チェックツール</h1>
        <p>Word、Excel、PDF、PowerPointファイルの校正チェックを行います</p>
      </header>

      <main className="app-main">
        {state.error && (
          <div className="error-message">
            <h3>エラー</h3>
            <p>{state.error}</p>
            <button onClick={resetResults} className="retry-btn">
              リセット
            </button>
          </div>
        )}

        {!state.isChecking && !state.checkResults && (
          <div className="upload-section">
            <h2>ファイルを選択してください</h2>
            <FileUploader
              onFilesSelected={handleFilesSelected}
              isLoading={state.isChecking}
              maxFiles={state.config?.max_files_count}
              maxFileSize={state.config?.max_file_size}
              supportedExtensions={state.config?.supported_extensions}
            />
          </div>
        )}

        {state.isChecking && (
          <div className="loading-message">
            <p>ドキュメントを解析中...</p>
          </div>
        )}

        {state.checkResults && (
          <div className="results-section">
            <CheckResults
              results={state.checkResults}
              isLoading={state.isChecking}
            />
            <div className="actions">
              <button onClick={resetResults} className="new-check-btn">
                新しいチェックを開始
              </button>
            </div>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>&copy; 2025 ドキュメント事前チェックツール</p>
      </footer>
    </div>
  );
}

export default App;
