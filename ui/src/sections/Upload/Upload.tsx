import React, {useState, useEffect, useRef} from 'react';


import { UploadCard } from '.';

import {api} from '../../lib/api';

import {ErrorBox, useError } from '../../sections'

export const Upload = ({setScreen, setResponse, setProcessingFlag}: any) => {

    const [error, setError, clearError ] = useError();

    const timerRef = useRef<any>(null);
  

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
                `process/${operationId}`
            )
          
            const taskId = response.data.task_id;
            timerRef.current = setInterval( async () => {
                const response: any = await getStatus(taskId);
                if (response.data.state === 'SUCCESS'){
                    const data = response.data.details;
                    setResponse(data);
                    setScreen(false);
                    setProcessingFlag(false);
                    clearInterval(timerRef.current)
                }
            },5000)
        } catch (err) {
            // clearInterval(timerRef.current)
            setError(err.message);
            // throw new Error(err.message)
        }
    }

    
    const handleUpload =  (operationId: string, operationUrl: string) => {
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