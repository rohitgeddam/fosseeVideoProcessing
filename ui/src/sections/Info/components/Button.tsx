import React from 'react';

import styled from 'styled-components';
import { ButtonProps } from '../../../lib';

const Btn = styled.button`
    display: flex;
    justify-content: center;
    border: none;
    width: 100%;
    cursor: pointer;
    padding: 16px;
    background-color: #23120b;
    color: #f1f1f1;
    font-size: 14px;
    transition: width 1s, height 1s, transform 0.5s;

    letter-spacing: 3px;
    outline: none;
    margin-top: 10px;

    &:hover {
        color: #ffd66b;
        transform: scale(1.1);
    }
`;

const Children = styled.div`
    align-self: flex-end;
    margin-left: auto;
`;

export const Button: React.FC<ButtonProps> = ({ text, onClick, children }) => {
    return (
        <Btn onClick={onClick}>
            {text}
            <Children>{children}</Children>
        </Btn>
    );
};
