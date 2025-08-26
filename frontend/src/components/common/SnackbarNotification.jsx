import React from 'react'
import { Snackbar, Alert } from '@mui/material'

/**
 * Reusable snackbar notification component
 * @param {boolean} open - Whether snackbar is open
 * @param {string} message - Message to display
 * @param {string} severity - Alert severity (success, error, warning, info)
 * @param {Function} onClose - Close handler
 * @param {number} autoHideDuration - Auto-hide duration in milliseconds
 */
const SnackbarNotification = ({ 
  open, 
  message, 
  severity = 'info', 
  onClose, 
  autoHideDuration = 6000,
  ...props 
}) => {
  return (
    <Snackbar
      open={open}
      autoHideDuration={autoHideDuration}
      onClose={onClose}
      anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      {...props}
    >
      <Alert onClose={onClose} severity={severity} sx={{ width: '100%' }}>
        {message}
      </Alert>
    </Snackbar>
  )
}

export default SnackbarNotification