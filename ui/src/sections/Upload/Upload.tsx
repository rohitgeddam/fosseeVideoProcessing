import React, { useRef} from 'react';


import { UploadCard } from '.';

import {api, getTaskStatus} from '../../lib/api';

import {ErrorBox, useError } from '../../sections'

export const Upload = ({setScreen, setResponse, setProcessingFlag}: any) => {

    const [error, setError, clearError ] = useError();

    const timerRef = useRef<any>(null);
  

    const polling = async (operationId: string) => {
        try {
            const response = await api.get(
                `process/${operationId}`
            )
          
            const taskId = response.data.task_id;
            timerRef.current = setInterval( async () => {
                const response: any = await getTaskStatus(taskId);
                if (response.data.state === 'SUCCESS'){
                    const data = response.data.details;
                    setResponse(data);
                    setScreen(false);
                    setProcessingFlag(false);
                    clearInterval(timerRef.current)
                }
            },5000)
        } catch (err) {
            setError(err.message);
        }
    }

    
    const handleUpload =  (operationId: string) => {
        setProcessingFlag(true);
        polling(operationId);
    }
    
       
        
    return (
        <>
        { error.isError &&
            <ErrorBox text={error.message} onClick={clearError}/>
        }
        <UploadCard handleUpload={handleUpload}/>
        </>
    )
}