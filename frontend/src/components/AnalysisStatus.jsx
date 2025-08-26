import React from 'react'
import {
  Box,
  Typography,
  LinearProgress,
  Alert,
  Chip,
  Paper,
  List,
  ListItem,
  ListItemText,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow
} from '@mui/material'
import { ExpandMore } from '@mui/icons-material'
import { StatusChip } from './common'

/**
 * Reusable component for displaying task/analysis status
 */
function AnalysisStatus({ 
  taskStatus, 
  showLogs = true, 
  showSubTasks = true,
  variant = 'default' // 'default' | 'compact' | 'detailed'
}) {
  if (!taskStatus) {
    return (
      <Typography color="textSecondary">
        No analysis running
      </Typography>
    )
  }

  const getStatusColor = (status) => {
    const statusLower = status?.toLowerCase()
    if (['completed', 'success'].includes(statusLower)) return 'success'
    if (['error', 'failed'].includes(statusLower)) return 'error'
    if (['running', 'in_progress'].includes(statusLower)) return 'primary'
    if (['partial_completion'].includes(statusLower)) return 'warning'
    return 'default'
  }

  // Compact variant for embedded use
  if (variant === 'compact') {
    return (
      <Box>
        <Box display="flex" alignItems="center" gap={2} mb={1}>
          <Typography variant="body2" color="textSecondary">
            Status:
          </Typography>
          <Chip
            label={taskStatus.status}
            size="small"
            color={getStatusColor(taskStatus.status)}
          />
          {taskStatus.progress !== undefined && (
            <Typography variant="body2">
              {taskStatus.progress}%
            </Typography>
          )}
        </Box>
        {taskStatus.progress !== undefined && (
          <LinearProgress 
            variant="determinate" 
            value={taskStatus.progress || 0} 
          />
        )}
      </Box>
    )
  }

  return (
    <Box>
      {/* Task ID and Status */}
      <Box display="flex" alignItems="center" mb={2}>
        {taskStatus.task_id && (
          <Typography variant="body2" sx={{ mr: 2 }}>
            Task ID: {taskStatus.task_id.slice(0, 8)}
          </Typography>
        )}
        <StatusChip status={taskStatus.status} />
      </Box>
      
      {/* Progress Bar */}
      {taskStatus.progress !== undefined && (
        <Box mb={2}>
          <Typography variant="body2" gutterBottom>
            Progress: {taskStatus.progress}%
          </Typography>
          <LinearProgress 
            variant="determinate" 
            value={taskStatus.progress || 0} 
          />
        </Box>
      )}
      
      {/* Error Alert */}
      {taskStatus.error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {taskStatus.error}
        </Alert>
      )}
      
      {/* Success Alert */}
      {taskStatus.result && (
        <Alert severity="success" sx={{ mb: 2 }}>
          {typeof taskStatus.result === 'string' 
            ? taskStatus.result 
            : 'Analysis completed successfully'}
        </Alert>
      )}
      
      {/* Sub-tasks for multi-company analysis */}
      {showSubTasks && taskStatus.sub_task_statuses && taskStatus.sub_task_statuses.length > 0 && (
        <Accordion sx={{ mb: 2 }}>
          <AccordionSummary expandIcon={<ExpandMore />}>
            <Typography>Company Progress</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Company</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Progress</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {taskStatus.sub_task_statuses.map((subTask, index) => (
                    <TableRow key={subTask.task_id || index}>
                      <TableCell>
                        {subTask.company}
                        {subTask.ticker && ` (${subTask.ticker})`}
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={subTask.status}
                          size="small"
                          color={getStatusColor(subTask.status)}
                        />
                      </TableCell>
                      <TableCell>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <LinearProgress
                            variant="determinate"
                            value={subTask.progress || 0}
                            sx={{ width: '100px', mr: 1 }}
                          />
                          <Typography variant="caption">
                            {subTask.progress || 0}%
                          </Typography>
                        </Box>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </AccordionDetails>
        </Accordion>
      )}
      
      {/* Logs */}
      {showLogs && taskStatus.logs && taskStatus.logs.length > 0 && (
        <Paper sx={{ p: 2, maxHeight: '300px', overflow: 'auto', bgcolor: 'grey.50' }}>
          <Typography variant="subtitle2" gutterBottom>
            Execution Logs
          </Typography>
          <List dense>
            {taskStatus.logs.map((log, index) => (
              <ListItem key={index}>
                <ListItemText 
                  primary={log}
                  primaryTypographyProps={{ variant: 'body2' }}
                />
              </ListItem>
            ))}
          </List>
        </Paper>
      )}
    </Box>
  )
}

export default AnalysisStatus