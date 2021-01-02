import React, {useState, useRef} from 'react';

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



export const ShowInfo = ({data}: any) => {
    const [showDownloadBtn, setShowDownloadBtn] = useState(false)
    const [generateResultResponse, setGenerateResultResponse] = useState<any>(null)

    const timerRef = useRef<any>(null)

    const getStatus = async (taskId: string) => {
        try {
            const response = await api.get(
                `status/${taskId}`
            )
            return response;
        } catch (err) {
            throw new Error(err);
            
        }
    }



    const polling = async (operationId: string) => {
        try {
            const response = await api.get(
                `generate/${operationId}`
            )
          
            const taskId = response.data.task_id;

            timerRef.current = setInterval( async () => {
                
                const response = await getStatus(taskId);
               

                if (response.data.state === 'SUCCESS'){
                    const data = response.data.details;
                    console.log('data adfjoasdjf', data)
                    // setFlag(false);
                    setGenerateResultResponse(data);
                    setShowDownloadBtn(true);
                    clearInterval(timerRef.current)
                }
            },3000)
        } catch (err) {
            throw new Error(err);
            
        }
    }

    const handleGenerate = async () => {
        
        setShowDownloadBtn(false);
        polling(data.operationId)
    }

    return (
    <InfoDiv>
        <Heading>Info</Heading>
        <p>Total Chunks: <b>{data.chunks.length}</b></p>
        <p>Time Taken To Process: <b>{data.timeTaken}</b></p>
        <Button text={"Generate"} onClick={handleGenerate}></Button>
        {
            showDownloadBtn &&
            <a href={`http://localhost:8000${generateResultResponse.download}`} target="_blank" rel="noopener noreferrer" download>
                <Button text={"Download"}></Button>
            </a>
        }
    </InfoDiv>
    )
}


