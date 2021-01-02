import React, {useEffect, useState} from 'react';

export const useError = () => {
    const [error, setErrorMessage] = useState<any>({isError: false, message: ''});

    const setError = (message: string) => {
        setErrorMessage({isError: true, message: message})
    }

    const clearError = () => {
        setErrorMessage({isError: false, message: ''})
    }

    return [ error, setError, clearError ]
}
