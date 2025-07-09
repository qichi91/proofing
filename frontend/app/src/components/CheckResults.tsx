import React from 'react';
import type { CheckIssue, CheckResponse } from '../types/api';
import './CheckResults.css';

interface CheckResultsProps {
    results: CheckResponse | null;
    isLoading?: boolean;
}

const CheckResults: React.FC<CheckResultsProps> = ({
    results,
    isLoading = false,
}) => {
    if (isLoading) {
        return (
            <div className="check-results loading">
                <div className="loading-spinner">
                    <div className="spinner"></div>
                    <p>ファイルを解析中...</p>
                </div>
            </div>
        );
    }

    if (!results) {
        return null;
    }

    const totalIssues = results.results.reduce((sum, result) => sum + result.issues.length, 0);
    const successfulFiles = results.results.filter(result => result.status === 'success').length;
    const errorFiles = results.results.filter(result => result.status === 'error').length;

    const getSeverityColor = (severity: CheckIssue['severity']) => {
        switch (severity) {
            case 'error':
                return '#dc3545';
            case 'warning':
                return '#ffc107';
            case 'info':
                return '#17a2b8';
            default:
                return '#6c757d';
        }
    };

    const getSeverityIcon = (severity: CheckIssue['severity']) => {
        switch (severity) {
            case 'error':
                return '❌';
            case 'warning':
                return '⚠️';
            case 'info':
                return 'ℹ️';
            default:
                return '📝';
        }
    };

    const downloadResults = () => {
        const dataStr = JSON.stringify(results, null, 2);
        const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);

        const exportFileDefaultName = `check-results-${new Date().toISOString().split('T')[0]}.json`;

        const linkElement = document.createElement('a');
        linkElement.setAttribute('href', dataUri);
        linkElement.setAttribute('download', exportFileDefaultName);
        linkElement.click();
    };

    return (
        <div className="check-results">
            <div className="results-header">
                <h2>チェック結果</h2>
                <button onClick={downloadResults} className="download-btn">
                    結果をダウンロード
                </button>
            </div>

            <div className="results-summary">
                <div className="summary-card">
                    <h3>概要</h3>
                    <div className="summary-stats">
                        <div className="stat">
                            <span className="stat-label">総ファイル数:</span>
                            <span className="stat-value">{results.total_files}</span>
                        </div>
                        <div className="stat">
                            <span className="stat-label">処理済み:</span>
                            <span className="stat-value">{results.processed_files}</span>
                        </div>
                        <div className="stat">
                            <span className="stat-label">成功:</span>
                            <span className="stat-value success">{successfulFiles}</span>
                        </div>
                        <div className="stat">
                            <span className="stat-label">エラー:</span>
                            <span className="stat-value error">{errorFiles}</span>
                        </div>
                        <div className="stat">
                            <span className="stat-label">総問題数:</span>
                            <span className="stat-value warning">{totalIssues}</span>
                        </div>
                    </div>
                </div>
            </div>

            <div className="results-list">
                {results.results.map((result, index) => (
                    <div key={index} className={`result-card ${result.status}`}>
                        <div className="result-header">
                            <h3>{result.filename}</h3>
                            <span className={`status-badge ${result.status}`}>
                                {result.status === 'success' ? '✅ 成功' : '❌ エラー'}
                            </span>
                        </div>

                        {result.status === 'success' && (
                            <div className="file-stats">
                                <div className="stat-item">
                                    <span>文字数: {result.character_count}</span>
                                </div>
                                <div className="stat-item">
                                    <span>行数: {result.line_count}</span>
                                </div>
                                <div className="stat-item">
                                    <span>単語数: {result.word_count}</span>
                                </div>
                                <div className="stat-item">
                                    <span>問題数: {result.issues.length}</span>
                                </div>
                            </div>
                        )}

                        {result.status === 'error' && result.error_message && (
                            <div className="error-message">
                                <p>エラー: {result.error_message}</p>
                            </div>
                        )}

                        {result.issues.length > 0 && (
                            <div className="issues-list">
                                <h4>検出された問題</h4>
                                {result.issues.map((issue, issueIndex) => (
                                    <div key={issueIndex} className="issue-item">
                                        <div className="issue-header">
                                            <span
                                                className="severity-icon"
                                                style={{ color: getSeverityColor(issue.severity) }}
                                            >
                                                {getSeverityIcon(issue.severity)}
                                            </span>
                                            <span className="issue-type">{issue.type}</span>
                                            <span className="issue-line">行 {issue.line}</span>
                                        </div>
                                        <div className="issue-message">{issue.message}</div>
                                        {issue.suggestion && (
                                            <div className="issue-suggestion">
                                                💡 提案: {issue.suggestion}
                                            </div>
                                        )}
                                        <div className="issue-rule">ルール: {issue.rule}</div>
                                    </div>
                                ))}
                            </div>
                        )}

                        {result.status === 'success' && result.issues.length === 0 && (
                            <div className="no-issues">
                                <p>✨ 問題は見つかりませんでした！</p>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export { CheckResults as default };
