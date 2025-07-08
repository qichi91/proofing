import axios from 'axios';
import type { AxiosResponse, AxiosError } from 'axios';
import type { CheckResponse, HealthResponse, ConfigResponse } from '../types/api';

// APIベースURL（環境変数から取得、デフォルトは開発環境のURL）
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Axiosインスタンスの作成
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: 60000, // 60秒のタイムアウト（大きなファイルの処理に対応）
    headers: {
        'Content-Type': 'application/json',
    },
});

// リクエストインターセプター（ログ等）
apiClient.interceptors.request.use(
    (config) => {
        console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
    },
    (error) => {
        console.error('API Request Error:', error);
        return Promise.reject(error);
    }
);

// レスポンスインターセプター（エラーハンドリング）
apiClient.interceptors.response.use(
    (response: AxiosResponse) => {
        console.log(`API Response: ${response.status} ${response.config.url}`);
        return response;
    },
    (error: AxiosError) => {
        console.error('API Error:', error);
        return Promise.reject(error);
    }
);

// API関数定義
export const api = {
    // ヘルスチェック
    health: async (): Promise<HealthResponse> => {
        const response = await apiClient.get<HealthResponse>('/health');
        return response.data;
    },

    // 設定情報取得
    config: async (): Promise<ConfigResponse> => {
        const response = await apiClient.get<ConfigResponse>('/config');
        return response.data;
    },

    // ファイルチェック実行
    checkFiles: async (files: File[]): Promise<CheckResponse> => {
        const formData = new FormData();

        files.forEach((file) => {
            formData.append('files', file);
        });

        const response = await apiClient.post<CheckResponse>('/check', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
            // アップロードの進捗を監視する場合
            onUploadProgress: (progressEvent) => {
                if (progressEvent.total) {
                    const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    console.log(`Upload progress: ${progress}%`);
                }
            },
        });

        return response.data;
    },

    // 簡単なヘルスチェック
    ping: async (): Promise<{ message: string }> => {
        const response = await apiClient.get<{ message: string }>('/');
        return response.data;
    },
};

export default apiClient;
