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
  const [info, setInfo] = useState(null)
  
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
  
  // Create default ratio_rules.md when company and ticker are entered
  useEffect(() => {
    const createDefaultRatioRules = async () => {
      if (company && ticker && !info) {
        try {
          // Check if ratio rules exist by trying to get ratios
          const response = await analysisAPI.getRatios(ticker)
          if (response.data) {
            setInfo(`Default ratio configuration loaded for ${ticker}`)
          }
        } catch (error) {
          // Ratios don't exist yet, they'll be created when analysis starts
          console.log('Ratio rules will be created when analysis starts')
        }
      }
    }
    createDefaultRatioRules()
  }, [company, ticker])
  
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
    setInfo(null)
    console.log('Starting analysis for:', company, ticker)
    
    try {
      const response = await analysisAPI.startSingle({ company, ticker })
      console.log('Analysis started:', response.data)
      
      if (response.data.task_id) {
        startTask(response.data.task_id, {
          task_id: response.data.task_id,
          status: TASK_STATUS.INITIALIZING,
          progress: 0,
          logs: ['Starting analysis...'],
        })
        
        // Show info if ratio rules were created
        if (response.data.ratio_rules_created) {
          setInfo(`Default ratio_rules.md file created for ${ticker}`)
        }
      } else {
        console.error('No task_id in response:', response.data)
        setError(response.data.message || 'Failed to start analysis')
        
        // Show info about ratio rules creation even if analysis can't start
        if (response.data.ratio_rules_created) {
          setInfo(`Default ratio_rules.md file created for ${ticker}. ${response.data.message || ''}`)
        }
      }
    } catch (error) {
      console.error('Error starting analysis:', error)
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
    setInfo(null)
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
                  placeholder="e.g., Insig AI"
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
              
              {info && (
                <Alert severity="info" sx={{ mt: 2 }}>
                  {info}
                </Alert>
              )}
              
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