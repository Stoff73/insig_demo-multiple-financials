import React from 'react'
import { Box, Paper, Typography } from '@mui/material'

/**
 * Reusable empty state component
 * @param {ReactNode} icon - Icon to display
 * @param {string} title - Main message
 * @param {string} subtitle - Secondary message
 * @param {ReactNode} action - Optional action button
 */
const EmptyState = ({ icon, title, subtitle, action }) => {
  return (
    <Paper sx={{ p: 4, textAlign: 'center' }}>
      {icon && (
        <Box sx={{ fontSize: 60, color: 'text.secondary', mb: 2 }}>
          {React.cloneElement(icon, { sx: { fontSize: 'inherit' } })}
        </Box>
      )}
      <Typography variant="h6" color="textSecondary">
        {title}
      </Typography>
      {subtitle && (
        <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
          {subtitle}
        </Typography>
      )}
      {action && (
        <Box sx={{ mt: 3 }}>
          {action}
        </Box>
      )}
    </Paper>
  )
}

export default EmptyState