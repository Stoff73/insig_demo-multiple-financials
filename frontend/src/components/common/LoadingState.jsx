import React from 'react'
import { Box, CircularProgress, Typography } from '@mui/material'

/**
 * Reusable loading state component
 * @param {string} message - Optional loading message
 * @param {boolean} fullHeight - Whether to use full viewport height
 */
const LoadingState = ({ message = 'Loading...', fullHeight = true }) => {
  return (
    <Box
      display="flex"
      flexDirection="column"
      justifyContent="center"
      alignItems="center"
      minHeight={fullHeight ? '60vh' : '200px'}
      gap={2}
    >
      <CircularProgress />
      {message && (
        <Typography variant="body2" color="textSecondary">
          {message}
        </Typography>
      )}
    </Box>
  )
}

export default LoadingState