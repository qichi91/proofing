import apiClient from './client';
import type { CheckResponse, HealthResponse, ConfigResponse } from '../types/api';

export class ApiService {
    // ヘルスチェック
    static async health(): Promise<HealthResponse> {
        const response = await apiClient.get<HealthResponse>('/health');
        return response.data;
    }

    // 設定情報取得
    static async getConfig(): Promise<ConfigResponse> {
        const response = await apiClient.get<ConfigResponse>('/config');
        return response.data;
    }

    // ドキュメントチェック
    static async checkDocuments(files: File[]): Promise<CheckResponse> {
        const formData = new FormData();

        files.forEach((file) => {
            formData.append('files', file);
        });

        const response = await apiClient.post<CheckResponse>('/check', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });

        return response.data;
    }
}

export default ApiService;
