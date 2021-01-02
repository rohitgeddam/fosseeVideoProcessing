import React, { useState , useRef } from 'react';

import styled from 'styled-components';

import  MicRecorder  from 'mic-recorder-to-mp3'

import { api } from '../../../lib/api'
import { ErrorBox, useError } from '../../../sections'

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlay, faStop } from '@fortawesome/free-solid-svg-icons'

const Upload= styled.div`
    display: flex;
    justify-content: center;
    border: none;
    width: 100%;
   
    align-items:center;
    background-color: transparent;
    outline: none;
`
const Btn = styled.button`
    border: none;
    background: transparent;
    outline: none;
    cursor: pointer;
    width: 100%;

    &:hover {
        transform: scale(1.2);
        color: #ffd66b;
    
    }
`



export const AudioUploadMic = ({chunkId}: any) => {
    const [error, setError, clearError ] = useError();
    const [isRecording, setIsRecording] = useState(false);

    const [isLoading, setIsLoading] = useState<boolean>(false);

    const recorder = useRef<any>(null);

    const handleAudioReupload = async (file: any) => {
        
       

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await api.post(
                `reupload/${chunkId}`,
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
            )
        } catch (err) {
            setError(err.message)
        }

        setIsLoading(false);
    }

    const startRecording = () => {
         recorder.current = new MicRecorder({bitRate: 64})

        recorder.current.start().then(() => {
            // something else
        }).catch((e: any) => {
            console.error(e);
        });
    }

    const stopRecording = () => {
        recorder.current
        .stop()
        .getMp3().then(([buffer, blob]: any) => {
            const file = new File(buffer, `${chunkId}.mp3`, {
                type: blob.type,
                lastModified: Date.now()
            });
            
            const player = new Audio(URL.createObjectURL(file));
            player.play();
            handleAudioReupload(file);
        }).catch((e: any) => {
        alert('We could not retrieve your message');
        console.log(e);
        });
    }

    const handleRecording = () => {
      
        if (!isRecording) {
            startRecording();
        } else {
            stopRecording();
        }

        setIsRecording( (state) => !state)
    }

    return (
        <>
        { error.isError &&
                <ErrorBox text={error.message} onClick={clearError}/>
            }

        <Upload>
            {
                !isRecording ? 
                <Btn onClick={handleRecording}>
                    <FontAwesomeIcon icon={faPlay}/>
                </Btn>
                :
                <Btn onClick={handleRecording}>
                    <FontAwesomeIcon icon={faStop}/>
                </Btn>
            }
        </Upload>
        </>
    )
}


