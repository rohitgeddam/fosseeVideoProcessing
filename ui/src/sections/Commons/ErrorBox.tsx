import React from 'react';
import ReactLoading from 'react-loading';

import styled from 'styled-components';

const Error = styled.div`
    /* display: flex;
    flex-direction: column;
    justify-content: center; */
    /* align-items: center; */
    padding: 25px;
    background: #d9534f;
    opacity: 0.7;
    color: #f7f7f7;
    width: 70%;
    position: fixed;
    top: 16px;
   
    right: -20px;
    border-radius: 20px;
    font-size: 18px;
    font-family: cursive;
    font-size: 24px;
    font-weight: 700;
    letter-spacing: 3px;
    cursor: pointer;
    transition: width 2s, height 2s, transform 2s;
`


export const ErrorBox = ({text, onClick}: any) => {
    return (
        <Error onClick={onClick}>
            {text}
        </Error>
    )
}


