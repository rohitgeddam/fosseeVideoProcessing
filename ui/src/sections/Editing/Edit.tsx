import React from 'react';
import styled from 'styled-components';

import { ResultsTable } from '.';
import { EditProps } from '../../lib';
import { ShowInfo } from '../Info';

const ProcessingResultsContainer = styled.div`
    display: flex;
    width: 100%;
    justify-content: center;
    align-items: flex-start;
`;

export const Edit: React.FC<EditProps> = ({ data }) => {
    return (
        <ProcessingResultsContainer>
            <ResultsTable data={data} />
            <ShowInfo data={data} />
        </ProcessingResultsContainer>
    );
};
