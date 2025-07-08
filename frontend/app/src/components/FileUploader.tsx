import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import './FileUploader.css';

interface FileUploaderProps {
    onFilesSelected: (files: File[]) => void;
    maxFiles?: number;
    maxFileSize?: number;
    supportedExtensions?: string[];
    isLoading?: boolean;
}

export const FileUploader: React.FC<FileUploaderProps> = ({
    onFilesSelected,
    maxFiles = 10,
    maxFileSize = 50 * 1024 * 1024, // 50MB
    supportedExtensions = ['.docx', '.doc', '.xlsx', '.xls', '.pdf', '.pptx', '.ppt'],
    isLoading = false,
}) => {
    const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);

    const onDrop = useCallback(
        (acceptedFiles: File[], rejectedFiles: any[]) => {
            // ファイルサイズと数の検証
            const validFiles = acceptedFiles.filter((file) => {
                if (file.size > maxFileSize) {
                    alert(`ファイル "${file.name}" がサイズ制限（${Math.round(maxFileSize / 1024 / 1024)}MB）を超えています。`);
                    return false;
                }
                return true;
            });

            if (uploadedFiles.length + validFiles.length > maxFiles) {
                alert(`アップロードできるファイル数の上限（${maxFiles}個）を超えています。`);
                return;
            }

            const newFiles = [...uploadedFiles, ...validFiles];
            setUploadedFiles(newFiles);
            onFilesSelected(newFiles);

            // 拒否されたファイルの警告
            if (rejectedFiles.length > 0) {
                const rejectedNames = rejectedFiles.map(({ file }) => file.name).join(', ');
                alert(`以下のファイルは対応していない形式です: ${rejectedNames}`);
            }
        },
        [uploadedFiles, maxFiles, maxFileSize, onFilesSelected]
    );

    const removeFile = (index: number) => {
        const newFiles = uploadedFiles.filter((_, i) => i !== index);
        setUploadedFiles(newFiles);
        onFilesSelected(newFiles);
    };

    const clearFiles = () => {
        setUploadedFiles([]);
        onFilesSelected([]);
    };

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
            'application/msword': ['.doc'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
            'application/vnd.ms-excel': ['.xls'],
            'application/pdf': ['.pdf'],
            'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx'],
            'application/vnd.ms-powerpoint': ['.ppt'],
        },
        disabled: isLoading,
        multiple: true,
    });

    const formatFileSize = (bytes: number) => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    return (
        <div className="file-uploader">
            <div
                {...getRootProps()}
                className={`dropzone ${isDragActive ? 'drag-active' : ''} ${isLoading ? 'loading' : ''}`}
            >
                <input {...getInputProps()} />
                <div className="dropzone-content">
                    <div className="upload-icon">📁</div>
                    {isLoading ? (
                        <p>ファイルを処理中...</p>
                    ) : isDragActive ? (
                        <p>ファイルをここにドロップしてください</p>
                    ) : (
                        <div>
                            <p>ファイルをドラッグ&amp;ドロップするか、クリックしてファイルを選択してください</p>
                            <p className="supported-formats">
                                対応形式: {supportedExtensions.join(', ')}
                            </p>
                            <p className="file-limits">
                                最大ファイル数: {maxFiles}個 | 最大ファイルサイズ: {Math.round(maxFileSize / 1024 / 1024)}MB
                            </p>
                        </div>
                    )}
                </div>
            </div>

            {uploadedFiles.length > 0 && (
                <div className="uploaded-files">
                    <div className="files-header">
                        <h3>アップロード予定のファイル ({uploadedFiles.length}個)</h3>
                        <button onClick={clearFiles} className="clear-button" disabled={isLoading}>
                            すべてクリア
                        </button>
                    </div>
                    <div className="files-list">
                        {uploadedFiles.map((file, index) => (
                            <div key={index} className="file-item">
                                <div className="file-info">
                                    <span className="file-name">{file.name}</span>
                                    <span className="file-size">{formatFileSize(file.size)}</span>
                                </div>
                                <button
                                    onClick={() => removeFile(index)}
                                    className="remove-button"
                                    disabled={isLoading}
                                >
                                    ✕
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};
