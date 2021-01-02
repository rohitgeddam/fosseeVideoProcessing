/* eslint-disable react/display-name */
import React, { useEffect, useState } from 'react';

import styled from 'styled-components';

import { Table } from 'antd';

import { BASE_URL, Chunk, ResultTableProps } from '../../../lib';
import { AudioUploadButton, AudioUploadMic } from '../../../sections';

const DataTableContainer = styled.div``;

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
        render: (link: string) => (
            <a href={`${BASE_URL}${link}`} target="_blank" rel="noopener noreferrer">
                view
            </a>
        ),
    },
    {
        title: 'Audio',
        dataIndex: 'audioChunkPath',
        key: 'audioChunkPath',
        render: (link: string) => (
            <a href={`${BASE_URL}${link}`} target="_blank" rel="noopener noreferrer">
                view
            </a>
        ),
    },
    {
        title: 'Swap Audio File',
        dataIndex: 'swapAudioFile',
        key: 'swapAudioFile',
        render: (chunkId: number) => <AudioUploadButton chunkId={chunkId} />,
    },
    {
        title: 'Swap Audio Mic',
        dataIndex: 'swapAudioMic',
        key: 'swapAudioMic',
        render: (chunkId: number) => <AudioUploadMic chunkId={chunkId} />,
    },
];

export const ResultsTable = ({ data }: ResultTableProps) => {
    const [dataSource, setDataSource] = useState<Chunk[] | null>(null);

    useEffect(() => {
        const source = data.chunks.map((chunk: Chunk) => {
            return {
                key: chunk.id,
                me: chunk.me,
                startTime: chunk.startTime,
                endTime: chunk.endTime,
                subtitleChunk: chunk.subtitleChunk,
                videoChunkPath: chunk.videoChunkPath,
                audioChunkPath: chunk.audioChunkPath,
                swapAudioFile: chunk.id,
                swapAudioMic: chunk.id,
                audioChunkLocalPath: chunk.audioChunkLocalPath,
                audioChunkName: chunk.audioChunkName,
                id: chunk.id,
                operationId: chunk.operationId,
                videoChunkLocalPath: chunk.videoChunkLocalPath,
                videoChunkName: chunk.videoChunkName,
            };
        });
        setDataSource(source);
    }, []);
    return (
        <DataTableContainer>
            <Table dataSource={dataSource!} columns={columns} />
        </DataTableContainer>
    );
};
