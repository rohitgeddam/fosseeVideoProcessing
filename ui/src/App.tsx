import React, {useState, useEffect, useRef} from 'react';
import styled from 'styled-components';

import { api } from './lib'
import { Result, Upload } from 'antd';

import { UploadCard, ResultsTable, ShowInfo, LoadingScreen} from './sections'


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
  
  const [uploadStageData, setUploadStageData] = useState({
    operationId: null,
    operationUrl: null, 
  })

  const [taskId, setTaskId] = useState(null);
  const [processingResult, setProcessingResult] = useState<null | any>(null);

  const timerRef = useRef<any>();
  const isProcessingRef = useRef<boolean>(false);

  const startPolling = async (taskId: string) => {
    try{
     
      const response = await api.get(
          `status/${taskId}`
      )
      console.log("RESPONSE TASKID", response)
      if ( response.data.state === 'SUCCESS')
        clearInterval(timerRef.current)
        setProcessingResult(response.data.details)
        isProcessingRef.current = false
      } catch (err) {
          // setError({isError: true, message: "Failed to upload files"})
          console.log(err)
          isProcessingRef.current = false
          clearInterval(timerRef.current)
      }
  }

  const startProcessingRequest = async () => {
   // start processing
   try{
    isProcessingRef.current = true
   
    const response = await api.get(
        `process/${uploadStageData.operationId}`,
    )
    
    const taskId = response.data.task_id
    setTaskId(taskId)
   
    if(taskId){
      // poll with this taskId.
      timerRef.current = setInterval(() => startPolling(taskId),3000)
    }
    } catch (err) {
        // setError({isError: true, message: "Failed to upload files"})
        console.log(err)
        // isProcessingRef.current = false
        // clearInterval(timerRef.current)
    }
  }



  useEffect( () => {
    if(uploadStageData.operationId) {
      startProcessingRequest();
    }
    return () => {
      clearInterval(timerRef.current)
    };

  }, [uploadStageData])
  

console.log("is processing", isProcessingRef.current)


  return (
    <Container className="App">
      {
        isProcessingRef.current && <LoadingScreen text="Loading"/>
      }
      {
        
        !uploadStageData.operationId && <UploadCard uploadFiles={setUploadStageData}/>
     
      }
     
      {
        processingResult && 
        <ProcessingResultsContainer>
          <ResultsTable result={processingResult} />
          <ShowInfo info={processingResult} operationId={uploadStageData.operationId}/>
        </ProcessingResultsContainer>
      }
     

    </Container>
  );
}

export default App;
