// API レスポンスの型定義
export interface CheckIssue {
    type: string;
    severity: 'error' | 'warning' | 'info';
    line: number;
    message: string;
    rule: string;
    suggestion?: string;
}

export interface FileCheckResult {
    filename: string;
    status: 'success' | 'error';
    text_length?: number;
    character_count?: number;
    line_count?: number;
    word_count?: number;
    issues: CheckIssue[];
    error_message?: string;
}

export interface CheckResponse {
    total_files: number;
    processed_files: number;
    results: FileCheckResult[];
}

export interface HealthResponse {
    status: string;
    timestamp: string;
    version: string;
    dependencies: {
        textract: boolean;
        textlint: boolean;
    };
}

export interface ConfigResponse {
    max_file_size: number;
    max_files_count: number;
    supported_extensions: string[];
    log_level: string;
}
