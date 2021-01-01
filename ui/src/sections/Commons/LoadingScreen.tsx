import React from 'react';

import styled from 'styled-components';

const Loading = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    background: #fdb827;
    color: #23120b;
    width: 100%;
    height: 100vh;
    position: absolute;
    top: 0;
    left: 0;
    font-size: 36px;


`


export const LoadingScreen = ({text}: any) => {
    return (
        <Loading>
            {text}
        </Loading>
    )
}


