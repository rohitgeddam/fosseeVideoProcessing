import React, { useState } from 'react';

import styled from 'styled-components';
import ReactLoading from 'react-loading';

import { api } from '../../../lib/api';
import { ErrorBox, useError } from '../../../sections';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFileUpload } from '@fortawesome/free-solid-svg-icons';
import { UploadBtnProps } from '../../../lib';

const Upload = styled.div`
    display: flex;
    justify-content: center;
    border: none;
    width: 100%;
    cursor: pointer;
    align-items: center;
    background-color: transparent;
    outline: none;

    label {
        display: flex;
    }
    &:hover {
        color: #ffd66b;
    }
    input {
        display: none;
    }
`;

export const AudioUploadButton: React.FC<UploadBtnProps> = ({ chunkId }) => {
    const [error, setError, clearError] = useError();

    const [isLoading, setIsLoading] = useState<boolean>(false);

    const handleAudioReupload = async (e: any): Promise<void> => {
        setIsLoading(true);
        const file = e.target.files[0];
        const formData = new FormData();
        formData.append('file', file, `${chunkId}.mp3`);
        try {
            await api.post(`reupload/${chunkId}`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
        } catch (err) {
            setError(err.message);
        }
        setIsLoading(false);
    };

    return (
        <>
            {error.isError && <ErrorBox text={error.message} onClick={clearError} />}
            <Upload>
                <label htmlFor={chunkId.toString()}>
                    <FontAwesomeIcon icon={faFileUpload} />
                    {isLoading && <ReactLoading type={'bars'} color={'#fdb827'} height={25} width={25} />}
                </label>
                <input id={chunkId.toString()} onChange={handleAudioReupload} type="file" />
            </Upload>
        </>
    );
};
