import React, {useState, useRef} from 'react';

import styled from 'styled-components';
import ReactLoading from 'react-loading';


import { api } from '../../lib';
import {Button} from './components';
import { useError, ErrorBox } from '../../sections'

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
    font-size: 24px;
    text-align: center;
`



export const ShowInfo = ({data}: any) => {
    const [showDownloadBtn, setShowDownloadBtn] = useState(false)
    const [compileResultResponse, setcompileResultResponse] = useState<any>(null)
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError, clearError ] = useError();


    const timerRef = useRef<any>(null)

    const getStatus = async (taskId: string) => {
        try {
            const response = await api.get(
                `status/${taskId}`
            )
            return response;
        } catch (err) {
            setError(err.message);
        }
    }



    const polling = async (operationId: string) => {
        try {
            const response = await api.get(
                `generate/${operationId}`
            )
          
            const taskId = response.data.task_id;

            timerRef.current = setInterval( async () => {
                
                const response: any = await getStatus(taskId);
               

                if (response.data.state === 'SUCCESS'){
                    const data = response.data.details;
                    console.log('data adfjoasdjf', data)
                    // setFlag(false);
                    setcompileResultResponse(data);
                    setIsLoading(false);
                    setShowDownloadBtn(true);
                    clearInterval(timerRef.current)
                }
            },3000)
        } catch (err) {
            setIsLoading(false);
            clearInterval(timerRef.current)
            setError(err.message);
        }
    }

    const handleCompile = async () => {
        

        setShowDownloadBtn(false);
        setIsLoading(true);
        polling(data.operationId)
    }

    return (
        <>
        { error.isError &&
                // <ErrorMessage onClick={clearError}>{error.message}</ErrorMessage>
                <ErrorBox text={error.message} onClick={clearError}/>
        }
    <InfoDiv>
        <Heading>Info</Heading>
        <p>Total Chunks: <b>{data.chunks.length}</b></p>
        <p>Time Taken To Process: <b>{data.timeTaken}</b></p>
        <Button text={"Compile"} onClick={handleCompile}>
        {
            isLoading &&
            <ReactLoading type={"bars"} color={"#ffd66b"} height={25} width={25} />

        }
        </Button>
        
        {
            showDownloadBtn &&
            <a href={`http://localhost:8000${compileResultResponse.download}`} target="_blank" rel="noopener noreferrer" download>
                <Button text={"Download"}></Button>
            </a>
        }
        
    </InfoDiv>
    </>
    )
}


