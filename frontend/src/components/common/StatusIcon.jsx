import React from 'react'
import {
  CheckCircle,
  Error,
  Schedule,
  Warning,
} from '@mui/icons-material'
import { CircularProgress } from '@mui/material'
import { TASK_STATUS } from '../../utils/constants'

/**
 * Reusable status icon component
 * @param {string} status - Status value
 * @param {Object} props - Additional props for the icon
 */
const StatusIcon = ({ status, ...props }) => {
  switch (status) {
    case TASK_STATUS.COMPLETED:
      return <CheckCircle color="success" {...props} />
    case TASK_STATUS.ERROR:
      return <Error color="error" {...props} />
    case TASK_STATUS.RUNNING:
      return <CircularProgress size={20} {...props} />
    case TASK_STATUS.PARTIAL_COMPLETION:
      return <Warning color="warning" {...props} />
    default:
      return <Schedule color="action" {...props} />
  }
}

export default StatusIcon