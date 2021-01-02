import React, { useState, useRef } from 'react';

import styled from 'styled-components';
import ReactLoading from 'react-loading';

import { api, BASE_URL, CompileResponseType, getTaskStatus, ShowInfoProps, TaskStatusResponse } from '../../lib';
import { Button } from './components';
import { useError, ErrorBox } from '../../sections';

const InfoDiv = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 10px;
    min-height: 200px;
    max-height: 400px;
    margin: 0 40px;
    min-width: 200px;
    max-width: 400px;
    font-size: 16px;
    box-shadow: 1px 5px 16px 1px rgba(0, 0, 0, 0.2);
    border-radius: 10px;
`;

const Heading = styled.div`
    width: 100%;
    color: black;
    background-color: #ffd66b;
    font-size: 24px;
    text-align: center;
    margin-bottom: 10px;
    letter-spacing: 3px;
`;

export const ShowInfo: React.FC<ShowInfoProps> = ({ data }) => {
    const [showDownloadBtn, setShowDownloadBtn] = useState<boolean>(false);
    const [compileResultResponse, setCompileResultResponse] = useState<CompileResponseType | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError, clearError] = useError();
    const timerRef = useRef<number | undefined>();

    const polling = async (operationId: number): Promise<void> => {
        try {
            const response = await api.get(`generate/${operationId}`);
            const taskId = response.data.task_id;
            timerRef.current = window.setInterval(async () => {
                const response: TaskStatusResponse = await getTaskStatus(taskId);

                if (response.state === 'SUCCESS') {
                    const data = (response.details as unknown) as CompileResponseType;
                    setCompileResultResponse(data);
                    setIsLoading(false);
                    setShowDownloadBtn(true);
                    window.clearInterval(timerRef.current);
                }
            }, 3000);
        } catch (err) {
            setIsLoading(false);
            window.clearInterval(timerRef.current);
            setError(err.message);
        }
    };

    const handleCompile = async () => {
        setShowDownloadBtn(false);
        setIsLoading(true);
        polling(data.operationId);
    };

    return (
        <>
            {error.isError && <ErrorBox text={error.message} onClick={clearError} />}
            <InfoDiv>
                <Heading>Info</Heading>
                <p>
                    Total Chunks: <b>{data.chunks.length}</b>
                </p>
                <p>
                    Time Taken To Process: <b>{parseFloat(data.timeTaken).toFixed(2)} sec</b>
                </p>
                <Button text={'Compile'} onClick={handleCompile}>
                    {isLoading && <ReactLoading type={'bars'} color={'#ffd66b'} height={25} width={25} />}
                </Button>

                {showDownloadBtn && compileResultResponse && (
                    <a
                        href={`${BASE_URL}${compileResultResponse!.download}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        download="result.mp4"
                    >
                        <Button text={'Download'}></Button>
                    </a>
                )}
            </InfoDiv>
        </>
    );
};
