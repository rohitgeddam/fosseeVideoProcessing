import React, {useState} from 'react';

import styled from 'styled-components';
import { api } from '../../lib';
import {Button} from './components';

const InfoDiv = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: space-between;

    min-height: 200px;
    max-height: 400px;
    margin: 0 40px;
    min-width: 200px;
    max-width: 400px;
    font-size: 16px;

`

const Heading = styled.div`
    width: 100%;
    color: black;
    background-color: #ffd66b;
    font-size: 20px;
    text-align: center;
`



export const ShowInfo = ({info, operationId}: any) => {
    const [showDownloadBtn, setShowDownloadBtn] = useState(false)
    // const [generateResultResponse, setGenerateResultResponse] = useState<any>(null)

    // const startPolling = async (taskId: string) => {
    //     isProcessingRef.current = true
    //     try{
         
    //       const response = await api.get(
    //           `status/${taskId}`
    //       )
    //       console.log("RESPONSE TASKID", response)
    //       if ( response.data.state === 'SUCCESS')
    //         clearInterval(timerRef.current)
    //         setGenerateResultResponse(response.data)
    //         isProcessingRef.current = false
    //       } catch (err) {
    //           // setError({isError: true, message: "Failed to upload files"})
    //           console.log(err)
    //           isProcessingRef.current = false
    //           clearInterval(timerRef.current)
    //       }
    //   }

    const generateRequest = async () => {
        try{
            const response = await api.get(`generate/${operationId}`)
            console.log(response.data.taskId)
            // start polling
            // timerRef.current = setInterval(()=> startPolling(response.data.taskId),3000)
        } catch (err) {
            console.log(err)
        }
    }
    return (
    <InfoDiv>
        <Heading>Info</Heading>
        <p>Total Chunks: <b>{info.chunks.length}</b></p>
        {/* <p>Time Taken To Process: <b>{info.timeTaken}</b></p> */}
        <Button text={"Generate"} onClick={generateRequest}></Button>
        {
            showDownloadBtn &&
            <Button text={"Download"} onClick={()=>console.log("download")}></Button>
        }
    </InfoDiv>
    )
}


