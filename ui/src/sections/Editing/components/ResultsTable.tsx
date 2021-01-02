import React, { useEffect, useState } from 'react';

import styled from 'styled-components';

import { Table } from 'antd';
import { AudioUploadButton,  AudioUploadMic } from '.';

const ResultsTableContainer = styled.div`



`

const columns = [
    {
        title: 'Sr. No',
        dataIndex: 'me',
        key: 'me',
      },
      {
        title: 'Start Time',
        dataIndex: 'startTime',
        key: 'startTime',
      },
      {
        title: 'End Time',
        dataIndex: 'endTime',
        key: 'endTime',
      },
      {
        title: 'Subtitle',
        dataIndex: 'subtitleChunk',
        key: 'subtitleChunk',
      },
      {
        title: 'Video',
        dataIndex: 'videoChunkPath',
        key: 'videoChunkPath',
        render: (link: string) => <a href={`http://localhost:8000${link}`} target="_blank">view</a>
      },
      {
        title: 'Audio',
        dataIndex: 'audioChunkPath',
        key: 'audioChunkPath',
        render: (link: string) => <a href={`http://localhost:8000${link}`} target="_blank">view</a>

      },
      {
        title: 'Swap Audio File',
        dataIndex: 'swapAudioFile',
        key: 'swapAudioFile',
        render: (chunkId: string) => <AudioUploadButton chunkId={chunkId}/>
      },
    {
      title: 'Swap Audio Mic',
      dataIndex: 'swapAudioMic',
      key: 'swapAudioMic',
      render: (chunkId: string) => <AudioUploadMic chunkId={chunkId}/>
    }
]

export const ResultsTable =  ({result}: any) => {

    const [dataSource, setDataSource] = useState<any>(null)
    // const [column, setColumn] = useState(null);

    useEffect(() => {
        const data = result.chunks.map((chunk: any) => {
            return {
                // key: chunk.me,
                // id: chunk.id,
                me: chunk.me,
                // operationId: chunk.operationId,
                startTime: chunk.startTime,
                endTime: chunk.endTime,
                subtitleChunk: chunk.subtitleChunk,
                // videoChunkName: chunk.videoChunkName,
                videoChunkPath: chunk.videoChunkPath,
                // audioChunkName: chunk.audioChunkName,
                audioChunkPath: chunk.audioChunkPath,
                swapAudioFile: chunk.id,
                swapAudioMic: chunk.id
            }
            
        })
        setDataSource(data);

    }, [])
    return (
        <ResultsTableContainer>
            <Table dataSource={dataSource} columns={columns}/>
        </ResultsTableContainer>
    )
}

