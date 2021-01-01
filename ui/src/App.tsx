import React, {useState, useEffect, useRef} from 'react';
import styled from 'styled-components';

import { api } from './lib'
// import { Result, Upload } from 'antd';

import {Upload, ResultsTable, ShowInfo, LoadingScreen} from './sections'


const Container = styled.div`
    display: flex;
    /* background: #292F36; */
    height: 100vh;
    width: 100%;
    padding: 20px;
    justify-content: center;
`

const Loading = styled.div`
  font-size: 50px;
  color: green;
`

const ProcessingResultsContainer = styled.div`

    display: flex;
    width: 100%;
    align-items: flex-start;


`

function App() {

  const [onUploadScreen, setOnUploadScreen] = useState(true);
  
 
  const [processingResponse, setProcessingResponse] = useState<null | any>(null);


  // const isProcessingRef = useRef<boolean>(false);
  const [isProcessing, setIsProcessing] = useState<null | boolean>(false);

  useEffect(()=> {
    console.log("App is running");
    return ( () => console.log("App is unmounting"))
  })
  
if (isProcessing){
  return <h1>Processing</h1>
}

if(onUploadScreen) {
  return (
    <Container className="App">
     
   
      <Upload setScreen={setOnUploadScreen} setResponse={setProcessingResponse} setProcessingFlag={setIsProcessing}/>
  
    </Container>
  );
}

return (
  <Container className="App">
   
    <h1>Result screen</h1>

  </Container>
);
}

export default App;


 {/* {
        processingResult && 
        <ProcessingResultsContainer>
          <ResultsTable result={processingResult} />
          <ShowInfo info={processingResult} operationId={uploadStageData.operationId}/>
        </ProcessingResultsContainer>
      }
      */}