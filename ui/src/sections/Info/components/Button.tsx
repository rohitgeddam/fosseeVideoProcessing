import React from 'react';

import styled from 'styled-components';

const Btn= styled.button`

    border: none;
    width: 100%;
    cursor: pointer;
    padding: 16px;
    background-color: #23120b;
    color: #f1f1f1;
    font-size: 16px;
    text-align: center;
    outline: none;
    margin: 10px 0;
    &:hover {
        color: #ffd66b;
    }
`

export const Button = ({text, onClick}: any) => {
    return (
    <Btn onClick={onClick}>
        {text}
    </Btn>
    )
}


