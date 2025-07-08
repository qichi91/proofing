import React from 'react';
import './LoadingSpinner.css';

interface LoadingSpinnerProps {
    message?: string;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
    message = 'ドキュメントを解析中...'
}) => {
    return (
        <div className="loading-container">
            <div className="loading-spinner">
                <div className="spinner"></div>
                <p className="loading-message">{message}</p>
            </div>
        </div>
    );
};

export default LoadingSpinner;
