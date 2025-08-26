import React from 'react'
import { Chip } from '@mui/material'
import { STATUS_COLORS, TASK_STATUS } from '../../utils/constants'

/**
 * Reusable status chip component
 * @param {string} status - Status value
 * @param {string} size - Chip size (small, medium)
 * @param {Object} sx - Additional styles
 */
const StatusChip = ({ status, size = 'small', ...props }) => {
  const color = STATUS_COLORS[status] || STATUS_COLORS.default
  
  return (
    <Chip
      label={status}
      color={color}
      size={size}
      {...props}
    />
  )
}

export default StatusChip