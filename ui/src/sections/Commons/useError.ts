import React, { useState } from 'react';
import { useErrorState, useErrorReturnType } from '../../lib';

export const useError = (): useErrorReturnType => {
    const [error, setErrorMessage] = useState<useErrorState>({ isError: false, message: '' });

    const setError = (message: string) => {
        setErrorMessage({ isError: true, message: message });
    };

    const clearError = () => {
        setErrorMessage({ isError: false, message: '' });
    };

    return [error, setError, clearError];
};
