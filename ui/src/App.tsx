import React, {useState, useEffect} from 'react';
import styled from 'styled-components';


import { Upload } from 'antd';

import { UploadCard } from './sections'


const Container = styled.div`
    display: flex;
    /* background: #292F36; */
    height: 100vh;
    justify-content: center;
`


function App() {
  
  const [uploadStageData, setUploadStageData] = useState({
    operationId: null,
    operationUrl: null, 
  })
  
  useEffect( () => {
    console.log(uploadStageData)
  }, [uploadStageData])
  return (
    <Container className="App">
      {
        !uploadStageData.operationId && 
        <UploadCard submitFiles={setUploadStageData}/>
      }
    </Container>
  );
}

export default App;
