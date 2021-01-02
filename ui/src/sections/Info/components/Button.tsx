import React from 'react';

import styled from 'styled-components';

const Btn= styled.button`
    display: flex;
    justify-content: center;
    border: none;
    width: 100%;
    cursor: pointer;
    padding: 16px;
    background-color: #23120b;
    color: #f1f1f1;
    font-size: 14px;
    
    outline: none;
    margin-top: 10px;

    &:hover {
        color: #ffd66b;
    }
`

const Children = styled.div`
    align-self: flex-end;
    margin-left: auto;
`


export const Button = ({text, onClick, children}: any) => {
    return (
    <Btn onClick={onClick}>
        {text}
        <Children>
            {children}
        </Children>
    
    </Btn>
    )
}


