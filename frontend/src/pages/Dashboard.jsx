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
      <Box sx={{ mb: 4 }}>
        <Typography 
          variant="h4" 
          gutterBottom
          sx={{ 
            fontWeight: 700,
            color: '#0A2540',
            mb: 1
          }}
        >
          Dashboard
        </Typography>
        <Typography variant="body2" sx={{ color: '#5E6C84' }}>
          Monitor your financial analysis tasks and reports in real-time
        </Typography>
      </Box>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <Card sx={{ 
            background: 'linear-gradient(135deg, #0A2540 0%, #1E3A5F 100%)',
            color: '#FFFFFF',
            position: 'relative',
            overflow: 'hidden',
            '&::before': {
              content: '""',
              position: 'absolute',
              top: -50,
              right: -50,
              width: 150,
              height: 150,
              borderRadius: '50%',
              background: 'rgba(0, 212, 255, 0.1)',
            }
          }}>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Box sx={{ 
                  p: 1, 
                  borderRadius: 1, 
                  background: 'rgba(0, 212, 255, 0.15)',
                  display: 'flex',
                  mr: 2
                }}>
                  <TrendingUp sx={{ color: '#00D4FF' }} />
                </Box>
                <Typography variant="body2" sx={{ opacity: 0.9 }}>
                  Total Analyses
                </Typography>
              </Box>
              <Typography variant="h3" sx={{ fontWeight: 700 }}>
                {tasks.length}
              </Typography>
              <Typography variant="caption" sx={{ opacity: 0.7 }}>
                All time
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card sx={{ 
            background: 'linear-gradient(135deg, #00C48C 0%, #009C6E 100%)',
            color: '#FFFFFF',
            position: 'relative',
            overflow: 'hidden',
            '&::before': {
              content: '""',
              position: 'absolute',
              top: -50,
              right: -50,
              width: 150,
              height: 150,
              borderRadius: '50%',
              background: 'rgba(255, 255, 255, 0.1)',
            }
          }}>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Box sx={{ 
                  p: 1, 
                  borderRadius: 1, 
                  background: 'rgba(255, 255, 255, 0.2)',
                  display: 'flex',
                  mr: 2
                }}>
                  <CheckCircle sx={{ color: '#FFFFFF' }} />
                </Box>
                <Typography variant="body2" sx={{ opacity: 0.9 }}>
                  Completed
                </Typography>
              </Box>
              <Typography variant="h3" sx={{ fontWeight: 700 }}>
                {tasks.filter(t => t.status === TASK_STATUS.COMPLETED).length}
              </Typography>
              <Typography variant="caption" sx={{ opacity: 0.7 }}>
                Successfully finished
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card sx={{ 
            border: '1px solid #E1E8ED',
            boxShadow: '0 4px 12px rgba(10, 37, 64, 0.08)',
          }}>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Box sx={{ 
                  p: 1, 
                  borderRadius: 1, 
                  background: 'rgba(0, 101, 255, 0.1)',
                  display: 'flex',
                  mr: 2
                }}>
                  <Folder sx={{ color: '#0065FF' }} />
                </Box>
                <Typography color="textSecondary" variant="body2">
                  Input Files
                </Typography>
              </Box>
              <Typography variant="h3" sx={{ fontWeight: 700, color: '#0A2540' }}>
                {inputFiles.length}
              </Typography>
              <Typography variant="caption" sx={{ color: '#5E6C84' }}>
                Documents ready
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card sx={{ 
            border: '1px solid #E1E8ED',
            boxShadow: '0 4px 12px rgba(10, 37, 64, 0.08)',
          }}>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Box sx={{ 
                  p: 1, 
                  borderRadius: 1, 
                  background: 'rgba(0, 212, 255, 0.1)',
                  display: 'flex',
                  mr: 2
                }}>
                  <Description sx={{ color: '#00D4FF' }} />
                </Box>
                <Typography color="textSecondary" variant="body2">
                  Reports
                </Typography>
              </Box>
              <Typography variant="h3" sx={{ fontWeight: 700, color: '#0A2540' }}>
                {outputFiles.length}
              </Typography>
              <Typography variant="caption" sx={{ color: '#5E6C84' }}>
                Generated reports
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ 
            p: 3, 
            height: '400px', 
            overflow: 'auto',
            background: '#FFFFFF',
            border: '1px solid #E1E8ED'
          }}>
            <Typography 
              variant="h6" 
              gutterBottom
              sx={{ 
                fontWeight: 600,
                color: '#0A2540',
                mb: 2,
                display: 'flex',
                alignItems: 'center',
                gap: 1
              }}
            >
              <Box sx={{ 
                width: 4, 
                height: 24, 
                background: 'linear-gradient(180deg, #00D4FF 0%, #0065FF 100%)',
                borderRadius: 1,
                mr: 1
              }} />
              Recent Analyses
            </Typography>
            <List>
              {tasks
                .filter(task => task.status !== 'error' || (task.error && !task.error.includes('timed out')))
                .sort((a, b) => {
                  // Sort by created_at date, most recent first
                  const dateA = new Date(a.created_at || 0)
                  const dateB = new Date(b.created_at || 0)
                  return dateB - dateA
                })
                .slice(0, 5)
                .map((task) => (
                  <ListItem key={task.task_id}>
                    <Box display="flex" alignItems="center" width="100%">
                      <StatusIcon status={task.status} />
                      <ListItemText
                        primary={`${task.company || 'Company'} (${task.ticker || 'N/A'})`}
                        secondary={
                          task.created_at 
                            ? formatDate(task.created_at)
                            : task.task_id.slice(0, 8)
                        }
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
          <Paper sx={{ 
            p: 3, 
            height: '400px', 
            overflow: 'auto',
            background: '#FFFFFF',
            border: '1px solid #E1E8ED'
          }}>
            <Typography 
              variant="h6" 
              gutterBottom
              sx={{ 
                fontWeight: 600,
                color: '#0A2540',
                mb: 2,
                display: 'flex',
                alignItems: 'center',
                gap: 1
              }}
            >
              <Box sx={{ 
                width: 4, 
                height: 24, 
                background: 'linear-gradient(180deg, #00D4FF 0%, #0065FF 100%)',
                borderRadius: 1,
                mr: 1
              }} />
              Latest Reports
            </Typography>
            <List>
              {outputFiles
                .filter(file => {
                  // Filter for key report files only
                  const name = file.name.toLowerCase()
                  return name.includes('valuation') || 
                         name.includes('ownership') || 
                         name.includes('earning_quality') || 
                         name.includes('balancesheet_durability') || 
                         name.includes('final_analysis')
                })
                .sort((a, b) => {
                  // Sort by modified date, most recent first
                  const dateA = new Date(a.modified || 0)
                  const dateB = new Date(b.modified || 0)
                  return dateB - dateA
                })
                .slice(0, 5)
                .map((file) => {
                  // Extract ticker and report type from filename
                  const match = file.name.match(/^([A-Z]+)_(.+)\.md$/)
                  const ticker = match ? match[1] : ''
                  const reportType = match ? match[2].replace(/_/g, ' ') : file.name
                  
                  return (
                    <ListItem key={file.name}>
                      <Description color="action" sx={{ mr: 2 }} />
                      <ListItemText
                        primary={`${ticker} - ${reportType}`}
                        secondary={`${formatFileSize(file.size)} - ${formatDate(file.modified)}`}
                      />
                    </ListItem>
                  )
                })}
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