import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import './FileUpload.css';

interface FileUploadProps {
    onFilesSelected: (files: File[]) => void;
    disabled?: boolean;
    maxFiles?: number;
    maxFileSize?: number;
    acceptedFormats?: string[];
}

const FileUpload: React.FC<FileUploadProps> = ({
    onFilesSelected,
    disabled = false,
    maxFiles = 10,
    maxFileSize = 50 * 1024 * 1024, // 50MB
    acceptedFormats = ['.docx', '.doc', '.xlsx', '.xls', '.pdf', '.pptx', '.ppt'],
}) => {
    const [selectedFiles, setSelectedFiles] = useState<File[]>([]);

    const onDrop = useCallback((acceptedFiles: File[]) => {
        setSelectedFiles(acceptedFiles);
        onFilesSelected(acceptedFiles);
    }, [onFilesSelected]);

    const { getRootProps, getInputProps, isDragActive, fileRejections } = useDropzone({
        onDrop,
        disabled,
        maxFiles,
        maxSize: maxFileSize,
        accept: acceptedFormats.reduce((acc, format) => {
            acc[`application/${format.slice(1)}`] = [format];
            return acc;
        }, {} as Record<string, string[]>),
    });

    const removeFile = (index: number) => {
        const newFiles = selectedFiles.filter((_, i) => i !== index);
        setSelectedFiles(newFiles);
        onFilesSelected(newFiles);
    };

    const formatFileSize = (bytes: number): string => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    return (
        <div className="file-upload">
            <div
                {...getRootProps()}
                className={`dropzone ${isDragActive ? 'active' : ''} ${disabled ? 'disabled' : ''}`}
            >
                <input {...getInputProps()} />
                <div className="dropzone-content">
                    <div className="upload-icon">📁</div>
                    {isDragActive ? (
                        <p>ファイルをドロップしてください...</p>
                    ) : (
                        <div>
                            <p>ファイルをドラッグ&ドロップするか、クリックしてファイルを選択してください</p>
                            <p className="upload-hint">
                                対応形式: {acceptedFormats.join(', ')} | 最大ファイルサイズ: {formatFileSize(maxFileSize)} | 最大ファイル数: {maxFiles}
                            </p>
                        </div>
                    )}
                </div>
            </div>

            {fileRejections.length > 0 && (
                <div className="file-rejections">
                    <h4>アップロードできないファイル:</h4>
                    {fileRejections.map(({ file, errors }) => (
                        <div key={file.name} className="rejection-item">
                            <span>{file.name}</span>
                            <ul>
                                {errors.map((error) => (
                                    <li key={error.code}>{error.message}</li>
                                ))}
                            </ul>
                        </div>
                    ))}
                </div>
            )}

            {selectedFiles.length > 0 && (
                <div className="selected-files">
                    <h4>選択されたファイル:</h4>
                    <div className="file-list">
                        {selectedFiles.map((file, index) => (
                            <div key={`${file.name}-${index}`} className="file-item">
                                <div className="file-info">
                                    <span className="file-name">{file.name}</span>
                                    <span className="file-size">{formatFileSize(file.size)}</span>
                                </div>
                                <button
                                    type="button"
                                    onClick={() => removeFile(index)}
                                    className="remove-file"
                                    disabled={disabled}
                                >
                                    ×
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default FileUpload;
