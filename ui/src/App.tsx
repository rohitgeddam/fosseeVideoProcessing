import React, { useState } from 'react';

import styled from 'styled-components';

import { ProcessingResponseType } from './lib';
import { Upload, Edit, LoadingScreen } from './sections';

const Container = styled.div`
    display: flex;
    background: #f1f1f1;
    min-height: 100vh;
    width: 100%;
    padding: 20px;
    justify-content: center;
`;

const App: React.FC = () => {
    const [onUploadScreen, setOnUploadScreen] = useState<boolean>(true);

    const [processingResponse, setProcessingResponse] = useState<null | ProcessingResponseType>(null);

    const [isProcessing, setIsProcessing] = useState<boolean>(false);

    if (isProcessing) {
        return <LoadingScreen text={'Please wait. Processing might take several minutes'} />;
    }

    if (onUploadScreen) {
        return (
            <Container className="App">
                <Upload
                    setScreen={setOnUploadScreen}
                    setResponse={setProcessingResponse}
                    setProcessingFlag={setIsProcessing}
                />
            </Container>
        );
    }

    return (
        <Container className="App">
            <Edit data={processingResponse!} />
        </Container>
    );
};

export default App;
