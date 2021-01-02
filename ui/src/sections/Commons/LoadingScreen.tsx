import React from 'react';
import ReactLoading from 'react-loading';

import styled from 'styled-components';

const Loading = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: #fdb827;
    color: #23120b;
    width: 100%;
    height: 100vh;
    position: absolute;
    top: 0;
    left: 0;
    font-size: 32px;
    font-family: cursive;


`


export const LoadingScreen = ({text}: any) => {
    return (
        <Loading>
            <ReactLoading type={"cylon"} color={"#000"} height={400} width={375} />
            {text}
        </Loading>
    )
}


