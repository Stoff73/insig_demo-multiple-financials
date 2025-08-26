import React, { useState, useEffect } from 'react'
import {
  Box,
  Button,
  Card,
  CardContent,
  Grid,
  TextField,
  Typography,
  Alert,
} from '@mui/material'
import {
  PlayArrow,
  Stop,
  Refresh,
} from '@mui/icons-material'
import { analysisAPI } from '../utils/api'
import { TASK_STATUS } from '../utils/constants'
import useTaskStatus from '../hooks/useTaskStatus'
import AnalysisStatus from '../components/AnalysisStatus'
import { useCompany } from '../contexts/CompanyContext'

function Analysis() {
  const { 
    company: sharedCompany, 
    ticker: sharedTicker, 
    setCompany: setSharedCompany, 
    setTicker: setSharedTicker 
  } = useCompany()
  
  const [company, setCompany] = useState(sharedCompany)
  const [ticker, setTicker] = useState(sharedTicker)
  const [error, setError] = useState(null)
  
  // Sync with shared context when local state changes
  useEffect(() => {
    setSharedCompany(company)
  }, [company, setSharedCompany])
  
  useEffect(() => {
    setSharedTicker(ticker)
  }, [ticker, setSharedTicker])
  
  // Update local state when shared context changes (e.g., from another tab)
  useEffect(() => {
    setCompany(sharedCompany)
  }, [sharedCompany])
  
  useEffect(() => {
    setTicker(sharedTicker)
  }, [sharedTicker])
  
  const {
    taskStatus,
    loading,
    startTask,
    stopTask,
    reset,
    isRunning
  } = useTaskStatus()

  const startAnalysis = async () => {
    setError(null)
    
    try {
      const response = await analysisAPI.startSingle({ company, ticker })
      
      startTask(response.data.task_id, {
        task_id: response.data.task_id,
        status: TASK_STATUS.INITIALIZING,
        progress: 0,
        logs: ['Starting analysis...'],
      })
    } catch (error) {
      setError('Failed to start analysis: ' + (error.response?.data?.detail || error.message))
    }
  }

  const handleStopAnalysis = async () => {
    if (!taskStatus?.task_id) return
    
    try {
      await analysisAPI.stopAnalysis(taskStatus.task_id)
      stopTask()
    } catch (error) {
      setError('Failed to stop analysis: ' + (error.response?.data?.detail || error.message))
    }
  }

  const resetForm = () => {
    reset()
    setError(null)
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Run Analysis
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Analysis Parameters
              </Typography>
              
              <Box sx={{ mb: 2 }}>
                <TextField
                  fullWidth
                  label="Company Name"
                  value={company}
                  onChange={(e) => setCompany(e.target.value)}
                  disabled={loading}
                  margin="normal"
                  placeholder="e.g., XP Power"
                />
                
                <TextField
                  fullWidth
                  label="Ticker Symbol"
                  value={ticker}
                  onChange={(e) => setTicker(e.target.value.toUpperCase())}
                  disabled={loading}
                  margin="normal"
                  placeholder="e.g., XPP"
                />
              </Box>
              
              <Box display="flex" gap={2}>
                <Button
                  variant="contained"
                  color="primary"
                  startIcon={<PlayArrow />}
                  onClick={startAnalysis}
                  disabled={loading || !company || !ticker}
                  fullWidth
                >
                  Start Analysis
                </Button>
                
                {loading && (
                  <Button
                    variant="outlined"
                    color="secondary"
                    startIcon={<Stop />}
                    onClick={handleStopAnalysis}
                  >
                    Stop
                  </Button>
                )}
                
                {taskStatus && !loading && (
                  <Button
                    variant="outlined"
                    startIcon={<Refresh />}
                    onClick={resetForm}
                  >
                    Reset
                  </Button>
                )}
              </Box>
              
              {error && (
                <Alert severity="error" sx={{ mt: 2 }}>
                  {error}
                </Alert>
              )}
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Execution Status
              </Typography>
              
              <AnalysisStatus taskStatus={taskStatus} showSubTasks={false} />
            </CardContent>
          </Card>
        </Grid>
        
      </Grid>
    </Box>
  )
}

export default Analysis