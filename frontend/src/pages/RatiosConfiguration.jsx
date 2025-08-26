import React, { useState, useEffect } from 'react'
import { useCompany } from '../contexts/CompanyContext'
import {
  Box,
  Paper,
  Typography,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Switch,
  TextField,
  Button,
  Alert,
  Chip,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material'
import {
  Save as SaveIcon,
  RestartAlt as ResetIcon,
  Info as InfoIcon,
} from '@mui/icons-material'
import { ratiosAPI } from '../utils/api'
import { RATIO_CATEGORIES, CATEGORY_ORDER } from '../utils/constants'
import { SnackbarNotification } from '../components/common'
import useSnackbar from '../hooks/useSnackbar'

function RatiosConfiguration() {
  const { 
    company: sharedCompany, 
    ticker: sharedTicker, 
    setCompany: setSharedCompany, 
    setTicker: setSharedTicker 
  } = useCompany()
  
  const [ratios, setRatios] = useState({})
  const [originalRatios, setOriginalRatios] = useState({})
  const [selectedCategory, setSelectedCategory] = useState(0)
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [hasChanges, setHasChanges] = useState(false)
  const [ticker, setTicker] = useState(sharedTicker || '')
  const [company, setCompany] = useState(sharedCompany || '')
  const [showTickerDialog, setShowTickerDialog] = useState(!sharedTicker || !sharedCompany)
  const { snackbar, showSuccess, showError, showWarning, closeSnackbar } = useSnackbar()
  
  // Sync local state with shared context
  useEffect(() => {
    if (sharedCompany && sharedTicker) {
      setCompany(sharedCompany)
      setTicker(sharedTicker)
      setShowTickerDialog(false)
    }
  }, [sharedCompany, sharedTicker])

  useEffect(() => {
    // Don't fetch ratios until ticker is provided
    if (ticker) {
      fetchRatios()
    }
  }, [ticker])

  useEffect(() => {
    // Check if there are any changes
    setHasChanges(JSON.stringify(ratios) !== JSON.stringify(originalRatios))
  }, [ratios, originalRatios])

  const fetchRatios = async () => {
    if (!ticker) {
      showWarning('Please enter a ticker symbol first')
      return
    }
    
    try {
      setLoading(true)
      const response = await ratiosAPI.getRatios(ticker)
      setRatios(response.data)
      setOriginalRatios(JSON.parse(JSON.stringify(response.data)))
    } catch (error) {
      console.error('Error fetching ratios:', error)
      showError('Failed to load ratio configurations')
    } finally {
      setLoading(false)
    }
  }

  const handleTickerSubmit = () => {
    if (!ticker || !company) {
      showWarning('Please enter both company name and ticker symbol')
      return
    }
    // Update shared context
    setSharedCompany(company)
    setSharedTicker(ticker)
    setShowTickerDialog(false)
    fetchRatios()
  }

  const handleToggleRatio = (category, ratioKey) => {
    setRatios(prev => ({
      ...prev,
      [category]: {
        ...prev[category],
        [ratioKey]: {
          ...prev[category][ratioKey],
          enabled: !prev[category][ratioKey].enabled
        }
      }
    }))
  }

  const handleThresholdChange = (category, ratioKey, thresholdType, value) => {
    const numValue = parseFloat(value)
    if (isNaN(numValue) && value !== '') return

    setRatios(prev => ({
      ...prev,
      [category]: {
        ...prev[category],
        [ratioKey]: {
          ...prev[category][ratioKey],
          thresholds: {
            ...prev[category][ratioKey].thresholds,
            [thresholdType]: value === '' ? '' : numValue
          }
        }
      }
    }))
  }

  const handleSpecialRangeChange = (category, ratioKey, field, value) => {
    const numValue = parseFloat(value)
    if (isNaN(numValue) && value !== '') return

    setRatios(prev => ({
      ...prev,
      [category]: {
        ...prev[category],
        [ratioKey]: {
          ...prev[category][ratioKey],
          thresholds: {
            ...prev[category][ratioKey].thresholds,
            [field]: value === '' ? '' : numValue
          }
        }
      }
    }))
  }

  const handleSave = async () => {
    if (!ticker) {
      showWarning('Please enter a ticker symbol first')
      return
    }
    
    try {
      setSaving(true)
      await ratiosAPI.updateRatios(ticker, ratios)
      setOriginalRatios(JSON.parse(JSON.stringify(ratios)))
      showSuccess(`Ratio configurations saved for ${ticker}. The ratio_rules.md file has been updated.`)
    } catch (error) {
      console.error('Error saving ratios:', error)
      showError('Failed to save ratio configurations')
    } finally {
      setSaving(false)
    }
  }

  const handleReset = () => {
    setRatios(JSON.parse(JSON.stringify(originalRatios)))
    showWarning('Changes discarded')
  }

  const getEnabledCount = (category) => {
    if (!ratios[category]) return 0
    return Object.values(ratios[category]).filter(r => r.enabled).length
  }

  const getTotalCount = (category) => {
    if (!ratios[category]) return 0
    return Object.keys(ratios[category]).length
  }

  const renderRatioRow = (category, ratioKey, ratioConfig) => {
    const isSpecialRange = ratioConfig.special_range
    const lowerIsBetter = ratioConfig.lower_is_better

    return (
      <TableRow key={ratioKey}>
        <TableCell>
          <Box display="flex" alignItems="center">
            <Switch
              checked={ratioConfig.enabled || false}
              onChange={() => handleToggleRatio(category, ratioKey)}
              color="primary"
            />
          </Box>
        </TableCell>
        <TableCell>
          <Box>
            <Typography variant="body2" fontWeight="bold">
              {ratioConfig.name}
            </Typography>
            <Typography variant="caption" color="textSecondary">
              {ratioConfig.description}
            </Typography>
          </Box>
        </TableCell>
        <TableCell align="center">
          {isSpecialRange ? (
            <Box display="flex" gap={1} alignItems="center">
              <TextField
                size="small"
                type="number"
                value={ratioConfig.thresholds?.pass_min || ''}
                onChange={(e) => handleSpecialRangeChange(category, ratioKey, 'pass_min', e.target.value)}
                disabled={!ratioConfig.enabled}
                sx={{ width: 70 }}
              />
              <Typography>-</Typography>
              <TextField
                size="small"
                type="number"
                value={ratioConfig.thresholds?.pass_max || ''}
                onChange={(e) => handleSpecialRangeChange(category, ratioKey, 'pass_max', e.target.value)}
                disabled={!ratioConfig.enabled}
                sx={{ width: 70 }}
              />
            </Box>
          ) : (
            <TextField
              size="small"
              type="number"
              value={ratioConfig.thresholds?.pass || ''}
              onChange={(e) => handleThresholdChange(category, ratioKey, 'pass', e.target.value)}
              disabled={!ratioConfig.enabled}
              sx={{ width: 100 }}
            />
          )}
        </TableCell>
        <TableCell align="center">
          {isSpecialRange ? (
            <Box display="flex" gap={1} alignItems="center">
              <Typography variant="body2">
                {'< ' + (ratioConfig.thresholds?.pass_min || 0) + ' or > ' + (ratioConfig.thresholds?.monitor_max || 0)}
              </Typography>
            </Box>
          ) : (
            <TextField
              size="small"
              type="number"
              value={ratioConfig.thresholds?.monitor || ''}
              onChange={(e) => handleThresholdChange(category, ratioKey, 'monitor', e.target.value)}
              disabled={!ratioConfig.enabled}
              sx={{ width: 100 }}
            />
          )}
        </TableCell>
        <TableCell align="center">
          {isSpecialRange ? (
            <TextField
              size="small"
              type="number"
              value={ratioConfig.thresholds?.monitor_max || ''}
              onChange={(e) => handleSpecialRangeChange(category, ratioKey, 'monitor_max', e.target.value)}
              disabled={!ratioConfig.enabled}
              sx={{ width: 100 }}
              InputProps={{
                startAdornment: <Typography variant="body2" sx={{ mr: 1 }}>{'>'}</Typography>
              }}
            />
          ) : (
            <Chip
              label={lowerIsBetter ? 
                `> ${ratioConfig.thresholds?.monitor || 0}` : 
                `< ${ratioConfig.thresholds?.monitor || 0}`
              }
              size="small"
              color="error"
              variant="outlined"
            />
          )}
        </TableCell>
        <TableCell align="center">
          <Tooltip title={lowerIsBetter ? "Lower values are better" : "Higher values are better"}>
            <IconButton size="small">
              <InfoIcon fontSize="small" />
            </IconButton>
          </Tooltip>
        </TableCell>
      </TableRow>
    )
  }

  if (loading && !showTickerDialog) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography>Loading ratio configurations...</Typography>
      </Box>
    )
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h4" gutterBottom>
            Financial Ratios Configuration
          </Typography>
          {ticker && company && (
            <Typography variant="subtitle1" color="text.secondary">
              {company} ({ticker})
            </Typography>
          )}
        </Box>
        <Box display="flex" gap={2}>
          {ticker && company && (
            <Button
              variant="outlined"
              onClick={() => setShowTickerDialog(true)}
            >
              Change Company
            </Button>
          )}
          <Button
            variant="outlined"
            startIcon={<ResetIcon />}
            onClick={handleReset}
            disabled={!hasChanges || saving}
          >
            Reset Changes
          </Button>
          <Button
            variant="contained"
            startIcon={<SaveIcon />}
            onClick={handleSave}
            disabled={!hasChanges || saving}
          >
            Save to ratio_rules.md
          </Button>
        </Box>
      </Box>

      {hasChanges && (
        <Alert severity="warning" sx={{ mb: 2 }}>
          You have unsaved changes. Click "Save to ratio_rules.md" to update the configuration file.
        </Alert>
      )}

      <Paper sx={{ width: '100%', mb: 2 }}>
        <Tabs
          value={selectedCategory}
          onChange={(e, newValue) => setSelectedCategory(newValue)}
          variant="scrollable"
          scrollButtons="auto"
        >
          {CATEGORY_ORDER.map((category, index) => (
            <Tab 
              key={category}
              label={
                <Box display="flex" alignItems="center" gap={1}>
                  <Typography>{RATIO_CATEGORIES[category]}</Typography>
                  <Chip 
                    label={`${getEnabledCount(category)}/${getTotalCount(category)}`}
                    size="small"
                    color={getEnabledCount(category) > 0 ? "primary" : "default"}
                  />
                </Box>
              }
            />
          ))}
        </Tabs>
      </Paper>

      {CATEGORY_ORDER.map((category, index) => (
        <Box
          key={category}
          hidden={selectedCategory !== index}
          sx={{ mt: 2 }}
        >
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              {RATIO_CATEGORIES[category]} Ratios
            </Typography>
            <Typography variant="body2" color="textSecondary" gutterBottom>
              Configure thresholds for PASS, MONITOR, and FAIL evaluations
            </Typography>

            <TableContainer sx={{ mt: 2 }}>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell width="80">Enabled</TableCell>
                    <TableCell>Ratio</TableCell>
                    <TableCell align="center" width="120">PASS</TableCell>
                    <TableCell align="center" width="120">MONITOR</TableCell>
                    <TableCell align="center" width="120">FAIL</TableCell>
                    <TableCell align="center" width="60">Info</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {ratios[category] && Object.entries(ratios[category]).map(([ratioKey, ratioConfig]) => 
                    renderRatioRow(category, ratioKey, ratioConfig)
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Box>
      ))}

      <SnackbarNotification
        open={snackbar.open}
        message={snackbar.message}
        severity={snackbar.severity}
        onClose={closeSnackbar}
      />

      {/* Ticker Input Dialog */}
      <Dialog open={showTickerDialog} maxWidth="sm" fullWidth>
        <DialogTitle>Select Company for Ratio Configuration</DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Please enter the company name and ticker symbol to configure ratios for that specific company.
          </Typography>
          <TextField
            fullWidth
            label="Company Name"
            value={company}
            onChange={(e) => {
              setCompany(e.target.value)
              // Don't update shared context until submit
            }}
            margin="normal"
            placeholder="e.g., XP Power"
          />
          <TextField
            fullWidth
            label="Ticker Symbol"
            value={ticker}
            onChange={(e) => {
              setTicker(e.target.value.toUpperCase())
              // Don't update shared context until submit
            }}
            margin="normal"
            placeholder="e.g., XPP"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleTickerSubmit} variant="contained" disabled={!ticker || !company}>
            Configure Ratios
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}

export default RatiosConfiguration