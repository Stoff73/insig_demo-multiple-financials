import React, { useState, useEffect } from 'react'
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  Paper,
  List,
  ListItem,
  ListItemText,
} from '@mui/material'
import {
  TrendingUp,
  Description,
  Folder,
  CheckCircle,
} from '@mui/icons-material'
import { fileAPI, analysisAPI } from '../utils/api'
import { formatFileSize, formatDate } from '../utils/formatters'
import { POLLING_INTERVALS, TASK_STATUS } from '../utils/constants'
import { StatusIcon, StatusChip, LoadingState } from '../components/common'
import usePolling from '../hooks/usePolling'

function Dashboard() {
  const [inputFiles, setInputFiles] = useState([])
  const [outputFiles, setOutputFiles] = useState([])
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)

  const fetchData = async () => {
    try {
      const [inputRes, outputRes, tasksRes] = await Promise.all([
        fileAPI.getInputFiles(),
        fileAPI.getOutputFiles(),
        analysisAPI.listTasks(),
      ])
      setInputFiles(inputRes.data.files || [])
      setOutputFiles(outputRes.data.files || [])
      setTasks(tasksRes.data || [])
      setLoading(false)
    } catch (error) {
      console.error('Error fetching data:', error)
      setLoading(false)
    }
  }

  // Use polling hook for automatic refresh (always enabled)
  usePolling(fetchData, POLLING_INTERVALS.DASHBOARD_REFRESH, true)

  if (loading) {
    return <LoadingState message="Loading dashboard..." />
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <TrendingUp color="primary" sx={{ mr: 1 }} />
                <Typography color="textSecondary" gutterBottom>
                  Total Analyses
                </Typography>
              </Box>
              <Typography variant="h3">
                {tasks.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <CheckCircle color="success" sx={{ mr: 1 }} />
                <Typography color="textSecondary" gutterBottom>
                  Completed
                </Typography>
              </Box>
              <Typography variant="h3">
                {tasks.filter(t => t.status === TASK_STATUS.COMPLETED).length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <Folder color="primary" sx={{ mr: 1 }} />
                <Typography color="textSecondary" gutterBottom>
                  Input Files
                </Typography>
              </Box>
              <Typography variant="h3">
                {inputFiles.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <Description color="secondary" sx={{ mr: 1 }} />
                <Typography color="textSecondary" gutterBottom>
                  Reports
                </Typography>
              </Box>
              <Typography variant="h3">
                {outputFiles.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '400px', overflow: 'auto' }}>
            <Typography variant="h6" gutterBottom>
              Recent Analyses
            </Typography>
            <List>
              {tasks.slice(0, 5).map((task) => (
                <ListItem key={task.task_id}>
                  <Box display="flex" alignItems="center" width="100%">
                    <StatusIcon status={task.status} />
                    <ListItemText
                      primary={`${task.company || 'XP Power'} (${task.year || '2024'})`}
                      secondary={task.task_id.slice(0, 8)}
                      sx={{ ml: 2 }}
                    />
                    <StatusChip status={task.status} />
                  </Box>
                </ListItem>
              ))}
              {tasks.length === 0 && (
                <ListItem>
                  <ListItemText 
                    primary="No analyses yet"
                    secondary="Start a new analysis from the Analysis page"
                  />
                </ListItem>
              )}
            </List>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '400px', overflow: 'auto' }}>
            <Typography variant="h6" gutterBottom>
              Latest Reports
            </Typography>
            <List>
              {outputFiles.slice(0, 5).map((file) => (
                <ListItem key={file.name}>
                  <Description color="action" sx={{ mr: 2 }} />
                  <ListItemText
                    primary={file.name}
                    secondary={`${formatFileSize(file.size)} - ${formatDate(file.modified)}`}
                  />
                </ListItem>
              ))}
              {outputFiles.length === 0 && (
                <ListItem>
                  <ListItemText 
                    primary="No reports generated"
                    secondary="Reports will appear here after analysis completion"
                  />
                </ListItem>
              )}
            </List>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  )
}

export default Dashboard