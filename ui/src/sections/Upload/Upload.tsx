import React, { useRef } from 'react';

import { UploadCard } from '.';

import { api, getTaskStatus, ProcessingResponseType, TaskStatusResponse, UploadProps } from '../../lib';

import { ErrorBox, useError } from '../../sections';

export const Upload: React.FC<UploadProps> = ({ setScreen, setResponse, setProcessingFlag }) => {
    const [error, setError, clearError] = useError();

    const timerRef = useRef<undefined | number>();

    const polling = async (operationId: number): Promise<void> => {
        try {
            const response = await api.get(`process/${operationId}`);

            const taskId = response.data.task_id;
            timerRef.current = window.setInterval(async () => {
                const response: TaskStatusResponse = await getTaskStatus(taskId);
                if (response.state === 'SUCCESS') {
                    const data: ProcessingResponseType = response.details;
                    setResponse(data);
                    setScreen(false);
                    setProcessingFlag(false);
                    window.clearInterval(timerRef.current);
                }
            }, 5000);
        } catch (err) {
            setError(err.message);
        }
    };

    const handleUpload = (operationId: number): void => {
        setProcessingFlag(true);
        polling(operationId);
    };

    return (
        <>
            {error.isError && <ErrorBox text={error.message} onClick={clearError} />}
            <UploadCard handleUpload={handleUpload} />
        </>
    );
};
