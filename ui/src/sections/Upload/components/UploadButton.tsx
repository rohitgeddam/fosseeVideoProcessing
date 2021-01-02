import React from 'react';
import styled from 'styled-components';
import { UploadButtonProps } from '../../../lib';

const ButtonContainer = styled.div`
    display: flex;
    flex-direction: column;
    margin: 10px;

    label {
        font-size: 20px;
    }

    input {
        border: none;
        padding: 5px 2px;
        background-color: transparent;
        color: blue;
    }
`;

export const UploadButton: React.FC<UploadButtonProps> = ({ label, onChange }) => {
    const handleChange = (e: any): void => {
        onChange(e.target.files[0]);
    };

    return (
        <ButtonContainer>
            <label>{label}</label>
            <input type="file" onChange={handleChange} />
        </ButtonContainer>
    );
};
