import React, { useState } from 'react';

import { api, UploadCardProps } from '../../../lib';

import styled from 'styled-components';

import { Divider } from 'antd';

import { UploadButton, useError, ErrorBox } from '../../../sections';

const Card = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    border: none;
    max-height: 600px;
    min-height: 400px;
    min-width: 400px;
    max-width: 600px;
    /* border: 1px solid black; */
    align-self: center;
    background-color: #ffffff;
    box-shadow: 5px 5px 10px 15px rgba(0, 0, 0, 0.2);
`;

const ButtonContainer = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 100%;
    min-height: 100px;
    max-height: 200px;
    justify-content: space-between;
    margin: 20px 0;
`;

const ProcessBtn = styled.button`
    width: 100%;
    padding: 20px;
    background-color: #292f36;
    border: none;
    cursor: pointer;
    color: #ffffff;
    font-size: 20px;
    letter-spacing: 4px;
`;

export const UploadCard: React.FC<UploadCardProps> = ({ handleUpload }) => {
    const [videoFile, setVideoFile] = useState('');
    const [srtFile, setSrtFile] = useState('');

    const [error, setError, clearError] = useError();

    const handleSubmit = async (e: React.MouseEvent<HTMLElement>): Promise<void> => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('video', videoFile);
        formData.append('srt', srtFile);

        try {
            const response = await api.post('upload/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            const operationId: number = response.data.operationId;
            clearError();
            handleUpload(operationId);
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <Card>
            <ButtonContainer>
                <UploadButton label={'Choose video file'} onChange={setVideoFile} />
                <Divider />
                <UploadButton label={'Choose srt file'} onChange={setSrtFile} />
            </ButtonContainer>
            {error.isError && <ErrorBox text={error.message} onClick={clearError} />}
            <ProcessBtn onClick={handleSubmit}>Upload Files</ProcessBtn>
        </Card>
    );
};
