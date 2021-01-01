import React, {useState, useEffect, useRef} from 'react';


import { UploadCard } from '.';

import {api} from '../../lib/api';

export const Upload = ({setScreen, setResponse, setProcessingFlag}: any) => {
    useEffect(()=> {
        console.log("Upload is running");
        return ( () => console.log("upload is unmounting"))
      })

    const timerRef = useRef<any>(null);
  

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
                `process/${operationId}`
            )
          
            const taskId = response.data.task_id;
            timerRef.current = setInterval( async () => {
                
                const response = await getStatus(taskId);
                console.log(response)

                if (response.data.state === 'SUCCESS'){
                    const data = response.data.details;
                    setResponse(data);
                    setScreen(false);
                    setProcessingFlag(false);
                    clearInterval(timerRef.current)
                }
            },5000)
        } catch (err) {
            throw new Error(err);
            
        }
    }

    
    const handleUpload =  (operationId: string, operationUrl: string) => {
        console.log(operationId, operationUrl)
        setProcessingFlag(true);
        polling(operationId);
    }
    
       
        
    return (
        <UploadCard handleUpload={handleUpload}/>
    )
}