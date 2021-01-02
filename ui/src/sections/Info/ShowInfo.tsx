import React, {useState, useRef} from 'react';

import styled from 'styled-components';
import ReactLoading from 'react-loading';


import { api, BASE_URL, getTaskStatus} from '../../lib';
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

    box-shadow: -5px 10px 5px 1px rgba(0,0,0,0.2)

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




    const polling = async (operationId: string) => {
        try {
            const response = await api.get(
                `generate/${operationId}`
            )
            const taskId = response.data.task_id;
            timerRef.current = setInterval( async () => { 
                const response: any = await getTaskStatus(taskId);
               
                if (response.data.state === 'SUCCESS'){
                    const data = response.data.details;
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
        { 
            error.isError &&
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
                    <a href={`${BASE_URL}${compileResultResponse.download}`} target="_blank" rel="noopener noreferrer" download="result.mp4">
                        <Button text={"Download"}></Button>
                    </a>
                }
                
            </InfoDiv>
        </>
    )
}


