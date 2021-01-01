import React, {useState, useEffect, useRef} from 'react';
import styled from 'styled-components';

import { api } from './lib'
import { Result, Upload } from 'antd';

import { UploadCard } from './sections'
import { ResultsTable } from './sections'


const Container = styled.div`
    display: flex;
    /* background: #292F36; */
    height: 100vh;
    justify-content: center;
`

const Loading = styled.div`
  font-size: 50px;
  color: green;
`


function App() {
  
  const [uploadStageData, setUploadStageData] = useState({
    operationId: null,
    operationUrl: null, 
  })

  const [taskId, setTaskId] = useState(null);
  const [processingResult, setProcessingResult] = useState<null | any>(null);

  const timer = useRef<any>();
  const isProcessing = useRef<boolean>(false);

  const startPolling = async (taskId: string) => {
    try{
     
      const response = await api.get(
          `status/${taskId}`
      )
      console.log("RESPONSE TASKID", response)
      if ( response.data.state === 'SUCCESS')
        clearInterval(timer.current)
        setProcessingResult(response.data.details)
        isProcessing.current = false
      } catch (err) {
          // setError({isError: true, message: "Failed to upload files"})
          console.log(err)
          clearInterval(timer.current)
      }

    
  }

  const startProcessingRequest = async () => {
   // start processing
   try{
    isProcessing.current = true
    const response = await api.get(
        `process/${uploadStageData.operationId}`,
    )
    
    const taskId = response.data.task_id
    setTaskId(taskId)
   
    if(taskId){
      // poll with this taskId.
      timer.current = setInterval(() => startPolling(taskId),3000)
    }
    } catch (err) {
        // setError({isError: true, message: "Failed to upload files"})
        console.log(err)
        clearInterval(timer.current)
    }
  }



  useEffect( () => {
    if(uploadStageData.operationId) {
      startProcessingRequest();
      
    }
    return () => {
      clearInterval(timer.current)
    };

  }, [uploadStageData])
  


if (isProcessing.current){
  return <h1>Processing...</h1>
}

  return (
    <Container className="App">
      {
        !uploadStageData.operationId && 
        <UploadCard uploadFiles={setUploadStageData}/>
      }
     
      {
        processingResult && <ResultsTable result={processingResult} />
      }
     

    </Container>
  );
}

export default App;
