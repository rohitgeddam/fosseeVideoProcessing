import React, { useEffect, useState } from 'react';

import styled from 'styled-components';

import { Table } from 'antd';

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

