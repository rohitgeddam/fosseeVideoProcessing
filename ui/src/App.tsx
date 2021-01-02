import React, {useState, useEffect, useRef} from 'react';

import styled from 'styled-components';


import {Upload, Edit, LoadingScreen} from './sections'


const Container = styled.div`
    display: flex;
    background: #f1f1f1;
    min-height: 100vh;
    width: 100%;
    padding: 20px;
    justify-content: center;
`



function App() {

  const [onUploadScreen, setOnUploadScreen] = useState(true);
  
 
  const [processingResponse, setProcessingResponse] = useState<null | any>(null);



  const [isProcessing, setIsProcessing] = useState<null | boolean>(false);

  useEffect(()=> {
    console.log("App is running");
    return ( () => console.log("App is unmounting"))
  })
  
if (isProcessing){
  return <LoadingScreen text={"Please wait. Processing might take several minutes"}/>
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
    <Edit data={processingResponse}/>
  </Container>
);
}

export default App;
