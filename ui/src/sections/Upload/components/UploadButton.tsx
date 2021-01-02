import React, {SyntheticEvent} from 'react';
import styled from 'styled-components';


// interface props {
//     label: string;
//     onChange: (arg0: any) =>  React.Dispatch<React.SetStateAction<null>>
// }

const ButtonContainer = styled.div`
    display: flex;
    flex-direction: column;
    margin: 10px;

    label {
        font-size: 20px;
    }

    input {
        border: none;
        padding: 5px 2px;
        background-color: transparent;
        color: blue;
    }
`

export const UploadButton = ( {label, onChange}: any ) => {

    const handleChange = (e: any) => {

        onChange(e.target.files[0])
    }

    return (

        <ButtonContainer>
            <label>{label}</label>
            <input type="file" onChange={handleChange}/>
        </ButtonContainer>

    )
}

