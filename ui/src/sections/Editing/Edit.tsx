import React from 'react';
import styled from 'styled-components';

import { ResultsTable } from '.'
import { ShowInfo } from '../Info'

const ProcessingResultsContainer = styled.div`

    display: flex;
    width: 100%;
    align-items: flex-start;


`

export const Edit = ({data}: any) => {
    return (
        <ProcessingResultsContainer>
            <ResultsTable result={data}/>
            <ShowInfo data={data}/>
        </ProcessingResultsContainer>
  
    )
}