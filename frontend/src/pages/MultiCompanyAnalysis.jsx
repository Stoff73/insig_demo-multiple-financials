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
  IconButton,
  FormControlLabel,
  Checkbox,
  Divider,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material'
import {
  PlayArrow,
  Stop,
  Add,
  Delete,
  Business,
  Assessment,
} from '@mui/icons-material'
import { analysisAPI, companyAPI } from '../utils/api'
import useTaskStatus from '../hooks/useTaskStatus'
import useApi from '../hooks/useApi'
import AnalysisStatus from '../components/AnalysisStatus'

function MultiCompanyAnalysis() {
  const [companies, setCompanies] = useState([
    { ticker: '', name: '' }
  ])
  const [year, setYear] = useState('2024')
  const [parallel, setParallel] = useState(false)
  const [error, setError] = useState(null)
  const [companyOutputs, setCompanyOutputs] = useState({})
  
  const { taskStatus, loading, startTask, stopTask, isRunning } = useTaskStatus()
  const { data: allCompanies = [], execute: fetchAllCompanies } = useApi(companyAPI.listCompanies)

  useEffect(() => {
    fetchAllCompanies()
  }, [])

  useEffect(() => {
    // Update company-specific outputs when task status changes
    if (taskStatus?.sub_task_statuses) {
      const outputs = {}
      for (const subTask of taskStatus.sub_task_statuses) {
        if (subTask.ticker && subTask.status === 'completed') {
          outputs[subTask.ticker] = {
            status: subTask.status,
            progress: subTask.progress
          }
        }
      }
      setCompanyOutputs(outputs)
    }
    
    // Refresh company list when analysis completes
    if (!isRunning && taskStatus?.status && 
        ['completed', 'error', 'partial_completion'].includes(taskStatus.status)) {
      fetchAllCompanies()
    }
  }, [taskStatus, isRunning, fetchAllCompanies])

  const handleAddCompany = () => {
    if (companies.length < 10) {
      setCompanies([...companies, { ticker: '', name: '' }])
    }
  }

  const handleRemoveCompany = (index) => {
    const newCompanies = companies.filter((_, i) => i !== index)
    setCompanies(newCompanies.length > 0 ? newCompanies : [{ ticker: '', name: '' }])
  }

  const handleCompanyChange = (index, field, value) => {
    const newCompanies = [...companies]
    newCompanies[index][field] = value
    setCompanies(newCompanies)
  }

  const startAnalysis = async () => {
    // Validate companies
    const validCompanies = companies.filter(c => c.ticker && c.name)
    if (validCompanies.length === 0) {
      setError('Please add at least one company with ticker and name')
      return
    }

    setError(null)
    setCompanyOutputs({})
    
    try {
      const response = await analysisAPI.startMulti({
        companies: validCompanies,
        year,
        parallel
      })
      
      startTask(response.data.task_id)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to start analysis')
    }
  }

  const handleStopAnalysis = async () => {
    if (!taskStatus?.task_id) return
    
    try {
      await analysisAPI.stopAnalysis(taskStatus.task_id)
      stopTask()
    } catch (err) {
      setError('Failed to stop analysis')
    }
  }

  const viewCompanyResults = (ticker) => {
    window.open(`/reports/company/${ticker}`, '_blank')
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Multi-Company Analysis
      </Typography>
      
      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Company Input Section */}
        <Grid item xs={12} md={7}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <Business sx={{ mr: 1, verticalAlign: 'middle' }} />
                Companies to Analyze
              </Typography>
              
              <Box sx={{ mb: 2 }}>
                {companies.map((company, index) => (
                  <Box key={index} sx={{ display: 'flex', gap: 2, mb: 2, alignItems: 'center' }}>
                    <TextField
                      label="Ticker"
                      value={company.ticker}
                      onChange={(e) => handleCompanyChange(index, 'ticker', e.target.value.toUpperCase())}
                      variant="outlined"
                      size="small"
                      sx={{ width: '120px' }}
                      disabled={loading}
                      placeholder="e.g., XPP"
                    />
                    <TextField
                      label="Company Name"
                      value={company.name}
                      onChange={(e) => handleCompanyChange(index, 'name', e.target.value)}
                      variant="outlined"
                      size="small"
                      sx={{ flex: 1 }}
                      disabled={loading}
                      placeholder="e.g., XP Power Limited"
                    />
                    <IconButton
                      onClick={() => handleRemoveCompany(index)}
                      disabled={loading || companies.length === 1}
                      color="error"
                      size="small"
                    >
                      <Delete />
                    </IconButton>
                  </Box>
                ))}
              </Box>
              
              <Button
                startIcon={<Add />}
                onClick={handleAddCompany}
                disabled={loading || companies.length >= 10}
                variant="outlined"
                size="small"
                sx={{ mb: 2 }}
              >
                Add Company ({companies.length}/10)
              </Button>
              
              <Divider sx={{ my: 2 }} />
              
              <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
                <TextField
                  label="Analysis Year"
                  value={year}
                  onChange={(e) => setYear(e.target.value)}
                  variant="outlined"
                  size="small"
                  sx={{ width: '120px' }}
                  disabled={loading}
                />
                
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={parallel}
                      onChange={(e) => setParallel(e.target.checked)}
                      disabled={loading}
                    />
                  }
                  label="Run in parallel"
                />
                
                <Box sx={{ flex: 1 }} />
                
                <Button
                  variant="contained"
                  color="primary"
                  startIcon={loading ? <Stop /> : <PlayArrow />}
                  onClick={loading ? handleStopAnalysis : startAnalysis}
                  disabled={!loading && companies.filter(c => c.ticker && c.name).length === 0}
                >
                  {loading ? 'Stop Analysis' : 'Start Analysis'}
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Status Section */}
        <Grid item xs={12} md={5}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <Assessment sx={{ mr: 1, verticalAlign: 'middle' }} />
                Analysis Status
              </Typography>
              
              <AnalysisStatus 
                taskStatus={taskStatus} 
                showLogs={true}
                showSubTasks={true}
                variant="detailed"
              />
            </CardContent>
          </Card>
        </Grid>

        {/* Existing Companies Section */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Existing Company Data
              </Typography>
              
              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Ticker</TableCell>
                      <TableCell align="center">Data Files</TableCell>
                      <TableCell align="center">Output Files</TableCell>
                      <TableCell align="center">Archives</TableCell>
                      <TableCell>Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {(allCompanies?.companies || allCompanies || []).map((company) => (
                      <TableRow key={company.ticker}>
                        <TableCell>
                          <Typography variant="body2" fontWeight="bold">
                            {company.ticker}
                          </Typography>
                        </TableCell>
                        <TableCell align="center">
                          {company.data_file_count || 0}
                        </TableCell>
                        <TableCell align="center">
                          {company.output_file_count || 0}
                        </TableCell>
                        <TableCell align="center">
                          {company.archive_count || 0}
                        </TableCell>
                        <TableCell>
                          <Button
                            size="small"
                            onClick={() => viewCompanyResults(company.ticker)}
                            disabled={!company.has_output}
                          >
                            View Results
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                    {allCompanies.length === 0 && (
                      <TableRow>
                        <TableCell colSpan={5} align="center">
                          <Typography variant="body2" color="textSecondary">
                            No companies found. Start by adding companies above.
                          </Typography>
                        </TableCell>
                      </TableRow>
                    )}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  )
}

export default MultiCompanyAnalysis