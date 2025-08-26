import { useState, useCallback } from 'react'

/**
 * Custom hook for managing snackbar notifications
 * @returns {Object} Snackbar state and control functions
 */
export const useSnackbar = () => {
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'info', // 'success' | 'error' | 'warning' | 'info'
  })

  const showSnackbar = useCallback((message, severity = 'info') => {
    setSnackbar({
      open: true,
      message,
      severity,
    })
  }, [])

  const showSuccess = useCallback((message) => {
    showSnackbar(message, 'success')
  }, [showSnackbar])

  const showError = useCallback((message) => {
    showSnackbar(message, 'error')
  }, [showSnackbar])

  const showWarning = useCallback((message) => {
    showSnackbar(message, 'warning')
  }, [showSnackbar])

  const showInfo = useCallback((message) => {
    showSnackbar(message, 'info')
  }, [showSnackbar])

  const closeSnackbar = useCallback(() => {
    setSnackbar(prev => ({ ...prev, open: false }))
  }, [])

  return {
    snackbar,
    showSnackbar,
    showSuccess,
    showError,
    showWarning,
    showInfo,
    closeSnackbar,
  }
}

export default useSnackbar