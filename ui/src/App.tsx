import React from 'react';
import styled from 'styled-components';


import { Upload } from 'antd';

import { UploadCard } from './sections'


const Container = styled.div`
    display: flex;
    background: #292F36;
    height: 100vh;
    justify-content: center;
`


function App() {
  
  return (
    <Container className="App">
      <UploadCard/>
    </Container>
  );
}

export default App;
