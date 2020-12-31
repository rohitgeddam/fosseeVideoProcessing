import React, { SyntheticEvent, useState } from 'react';


import { api } from '../../lib'

import styled from 'styled-components';

import { Divider } from 'antd';

import { UploadButton } from '.'

const Card = styled.div`
    display: flex;
    flex-direction: column;

    justify-content: space-between;
    align-items: center;

    max-height: 600px;
    min-height: 400px;
    min-width: 400px;
    max-width: 600px;
    border: 1px solid black;
    align-self: center;
    background-color: #FFFFFF;
    box-shadow: 5px 5px 10px 15px rgba(0,0,0,0.2);

`

const ButtonContainer = styled.div`
    display: flex;
    flex-direction: column;
    align-items:center;
    min-width: 100%;
    min-height: 100px;
    max-height: 200px;
    justify-content: space-between;
    margin: 20px 0;

`

const ProcessBtn = styled.button`
    width: 100%;
    padding: 20px;
    background-color: #292F36;
    border: none;
    cursor: pointer;
    color: #ffffff;
    font-size: 20px;
    letter-spacing: 4px;
`


  

export const UploadCard = () => {

    const [videoFile, setVideoFile] = useState('');
    const [srtFile, setSrtFile] = useState('');

    const handleSubmit = async (e: SyntheticEvent) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append("video", videoFile);
        formData.append("srt", srtFile);

        try{ 
            const response = await api.post(
                'upload/',
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }

            )
            const operationId = response.data.operationId;
            const operationUrl = response.data.operation_url;
            
        } catch (err) {
            console.log(err)
        }
        
    }
    
    return (
        <Card>
            <ButtonContainer>
                <UploadButton label={"Choose video file"} onChange={setVideoFile}/>
                <Divider/>
                <UploadButton label={"Choose srt file"} onChange={setSrtFile}/>
            </ButtonContainer>
            <ProcessBtn onClick={handleSubmit}>Process</ProcessBtn>
        </Card>
        
    )
}

