import React, { useState, useEffect } from 'react'
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  Paper,
  Tabs,
  Tab,
  Button,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Chip,
  CircularProgress,
  Alert,
  Snackbar,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Switch,
  FormControlLabel,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Divider,
  Tooltip,
  Badge,
} from '@mui/material'
import {
  Rule,
  Add,
  Edit,
  Delete,
  Save,
  Cancel,
  ExpandMore,
  CheckCircle,
  Warning,
  Error,
  Assignment,
  Settings,
  TrendingUp,
  AccountBalance,
  AttachMoney,
  Group,
  Flag,
} from '@mui/icons-material'
import { rulesAPI, configAPI } from '../utils/api'
import useApi from '../hooks/useApi'
import useSnackbar from '../hooks/useSnackbar'
import { SnackbarNotification } from '../components/common'

const categoryIcons = {
  valuation: <TrendingUp />,
  ownership: <Group />,
  earnings_quality: <AttachMoney />,
  balance_sheet: <AccountBalance />,
  red_flags: <Flag />,
}

const categoryNames = {
  valuation: 'Valuation Metrics',
  ownership: 'Ownership & Insider Signals',
  earnings_quality: 'Earnings Quality',
  balance_sheet: 'Balance Sheet Durability',
  red_flags: 'Red Flags & Warnings',
}

function RulesConfiguration() {
  const [selectedCategory, setSelectedCategory] = useState('valuation')
  const [editDialog, setEditDialog] = useState({ open: false, rule: null, category: null, ruleId: null })
  const [assignDialog, setAssignDialog] = useState({ open: false, rule: null, category: null, ruleId: null })
  const { snackbar, showSuccess, showError, closeSnackbar } = useSnackbar()
  
  const { data: rulesData, loading: rulesLoading, execute: fetchRules } = useApi(rulesAPI.getRules)
  const { data: tasksData, loading: tasksLoading, execute: fetchTasks } = useApi(configAPI.getTasks)
  
  const rules = rulesData || {}
  const tasks = tasksData || {}
  const loading = rulesLoading || tasksLoading

  useEffect(() => {
    fetchRules()
    fetchTasks()
  }, [])

  const fetchData = async () => {
    try {
      await Promise.all([fetchRules(), fetchTasks()])
    } catch (error) {
      showError('Failed to fetch configuration data')
      setSnackbar({ open: true, message: 'Failed to load rules', severity: 'error' })
    }
  }

  const handleCategoryChange = (event, newValue) => {
    setSelectedCategory(newValue)
  }

  const openEditDialog = (category, ruleId, rule) => {
    setEditDialog({ 
      open: true, 
      rule: rule ? { ...rule } : createNewRule(category), 
      category, 
      ruleId: ruleId || generateRuleId() 
    })
  }

  const createNewRule = (category) => {
    const baseRule = {
      name: 'New Rule',
      description: 'Rule description',
      category: category,
      enabled: true,
      applies_to_tasks: [],
    }

    if (category === 'red_flags') {
      return {
        ...baseRule,
        metric_type: 'qualitative',
        severity: 'medium',
        implication: 'Describe the implication',
      }
    } else {
      return {
        ...baseRule,
        metric_type: 'ratio',
        thresholds: {
          pass: { operator: '<', value: 10 },
          monitor: { operator: 'between', min: 10, max: 20 },
          fail: { operator: '>', value: 20 },
        },
        notes: '',
      }
    }
  }

  const generateRuleId = () => {
    return `rule_${Date.now()}`
  }

  const closeEditDialog = () => {
    setEditDialog({ open: false, rule: null, category: null, ruleId: null })
  }

  const saveRule = async () => {
    try {
      const { rule, category, ruleId } = editDialog
      const isNew = !rules[category]?.[ruleId]
      
      const endpoint = isNew 
        ? `/api/rules/${category}/${ruleId}`
        : `/api/rules/${category}/${ruleId}`
      
      const method = isNew ? 'post' : 'put'
      
      await axios[method](endpoint, rule)
      
      // Update local state
      const updatedRules = { ...rules }
      if (!updatedRules[category]) {
        updatedRules[category] = {}
      }
      updatedRules[category][ruleId] = rule
      setRules(updatedRules)
      
      setSnackbar({ 
        open: true, 
        message: `Rule ${isNew ? 'created' : 'updated'} successfully`, 
        severity: 'success' 
      })
      closeEditDialog()
    } catch (error) {
      console.error('Error saving rule:', error)
      setSnackbar({ open: true, message: 'Failed to save rule', severity: 'error' })
    }
  }

  const deleteRule = async (category, ruleId) => {
    if (!window.confirm('Are you sure you want to delete this rule?')) return
    
    try {
      await axios.delete(`/api/rules/${category}/${ruleId}`)
      
      const updatedRules = { ...rules }
      delete updatedRules[category][ruleId]
      setRules(updatedRules)
      
      setSnackbar({ open: true, message: 'Rule deleted successfully', severity: 'success' })
    } catch (error) {
      console.error('Error deleting rule:', error)
      setSnackbar({ open: true, message: 'Failed to delete rule', severity: 'error' })
    }
  }

  const toggleRuleEnabled = async (category, ruleId, enabled) => {
    try {
      const endpoint = enabled 
        ? `/api/rules/${category}/${ruleId}/enable`
        : `/api/rules/${category}/${ruleId}/disable`
      
      await axios.post(endpoint)
      
      const updatedRules = { ...rules }
      updatedRules[category][ruleId].enabled = enabled
      setRules(updatedRules)
      
      setSnackbar({ 
        open: true, 
        message: `Rule ${enabled ? 'enabled' : 'disabled'}`, 
        severity: 'success' 
      })
    } catch (error) {
      console.error('Error toggling rule:', error)
      setSnackbar({ open: true, message: 'Failed to update rule', severity: 'error' })
    }
  }

  const openAssignDialog = (category, ruleId, rule) => {
    setAssignDialog({ open: true, rule, category, ruleId })
  }

  const closeAssignDialog = () => {
    setAssignDialog({ open: false, rule: null, category: null, ruleId: null })
  }

  const assignRuleToTask = async (taskName) => {
    try {
      const { category, ruleId } = assignDialog
      await axios.post(`/api/rules/${category}/${ruleId}/assign`, { task_name: taskName })
      
      const updatedRules = { ...rules }
      if (!updatedRules[category][ruleId].applies_to_tasks) {
        updatedRules[category][ruleId].applies_to_tasks = []
      }
      if (!updatedRules[category][ruleId].applies_to_tasks.includes(taskName)) {
        updatedRules[category][ruleId].applies_to_tasks.push(taskName)
      }
      setRules(updatedRules)
      
      setSnackbar({ open: true, message: 'Rule assigned to task', severity: 'success' })
      closeAssignDialog()
    } catch (error) {
      console.error('Error assigning rule:', error)
      setSnackbar({ open: true, message: 'Failed to assign rule', severity: 'error' })
    }
  }

  const removeRuleFromTask = async (category, ruleId, taskName) => {
    try {
      await axios.post(`/api/rules/${category}/${ruleId}/unassign`, { task_name: taskName })
      
      const updatedRules = { ...rules }
      const taskIndex = updatedRules[category][ruleId].applies_to_tasks.indexOf(taskName)
      if (taskIndex > -1) {
        updatedRules[category][ruleId].applies_to_tasks.splice(taskIndex, 1)
      }
      setRules(updatedRules)
      
      setSnackbar({ open: true, message: 'Rule removed from task', severity: 'success' })
    } catch (error) {
      console.error('Error removing rule from task:', error)
      setSnackbar({ open: true, message: 'Failed to remove rule from task', severity: 'error' })
    }
  }

  const updateEditRule = (field, value) => {
    setEditDialog(prev => ({
      ...prev,
      rule: { ...prev.rule, [field]: value }
    }))
  }

  const updateThreshold = (status, field, value) => {
    setEditDialog(prev => ({
      ...prev,
      rule: {
        ...prev.rule,
        thresholds: {
          ...prev.rule.thresholds,
          [status]: {
            ...prev.rule.thresholds[status],
            [field]: value
          }
        }
      }
    }))
  }

  const renderThresholdIcon = (status) => {
    switch (status) {
      case 'pass':
        return <CheckCircle color="success" />
      case 'monitor':
        return <Warning color="warning" />
      case 'fail':
        return <Error color="error" />
      default:
        return null
    }
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    )
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Rules & Thresholds Configuration
      </Typography>
      
      <Paper sx={{ width: '100%', mb: 3 }}>
        <Tabs value={selectedCategory} onChange={handleCategoryChange}>
          {Object.keys(categoryNames).map(category => (
            <Tab 
              key={category}
              value={category}
              label={categoryNames[category]} 
              icon={categoryIcons[category]} 
              iconPosition="start"
            />
          ))}
        </Tabs>
      </Paper>

      <Box display="flex" justifyContent="flex-end" mb={2}>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => openEditDialog(selectedCategory, null, null)}
        >
          Add New Rule
        </Button>
      </Box>

      <Grid container spacing={3}>
        {rules[selectedCategory] && Object.entries(rules[selectedCategory]).map(([ruleId, rule]) => (
          <Grid item xs={12} key={ruleId}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
                  <Box display="flex" alignItems="center">
                    <Rule color="primary" sx={{ mr: 1 }} />
                    <Typography variant="h6">
                      {rule.name}
                    </Typography>
                    {!rule.enabled && (
                      <Chip label="Disabled" size="small" color="default" sx={{ ml: 1 }} />
                    )}
                  </Box>
                  <Box>
                    <FormControlLabel
                      control={
                        <Switch
                          checked={rule.enabled}
                          onChange={(e) => toggleRuleEnabled(selectedCategory, ruleId, e.target.checked)}
                        />
                      }
                      label="Enabled"
                    />
                    <IconButton
                      size="small"
                      onClick={() => openEditDialog(selectedCategory, ruleId, rule)}
                    >
                      <Edit />
                    </IconButton>
                    <IconButton
                      size="small"
                      onClick={() => openAssignDialog(selectedCategory, ruleId, rule)}
                    >
                      <Assignment />
                    </IconButton>
                    <IconButton
                      size="small"
                      color="error"
                      onClick={() => deleteRule(selectedCategory, ruleId)}
                    >
                      <Delete />
                    </IconButton>
                  </Box>
                </Box>
                
                <Typography variant="body2" color="textSecondary" paragraph>
                  {rule.description}
                </Typography>

                {rule.thresholds && (
                  <Box mb={2}>
                    <Typography variant="subtitle2" gutterBottom>
                      Thresholds:
                    </Typography>
                    <Grid container spacing={2}>
                      {Object.entries(rule.thresholds).map(([status, threshold]) => (
                        <Grid item xs={12} sm={4} key={status}>
                          <Box display="flex" alignItems="center">
                            {renderThresholdIcon(status)}
                            <Box ml={1}>
                              <Typography variant="caption" color="textSecondary">
                                {status.toUpperCase()}:
                              </Typography>
                              <Typography variant="body2">
                                {threshold.operator === 'between' 
                                  ? `${threshold.min} - ${threshold.max}`
                                  : threshold.criteria 
                                    ? threshold.criteria
                                    : `${threshold.operator} ${threshold.value}`}
                              </Typography>
                            </Box>
                          </Box>
                        </Grid>
                      ))}
                    </Grid>
                  </Box>
                )}

                {rule.severity && (
                  <Chip 
                    label={`Severity: ${rule.severity}`} 
                    size="small"
                    color={rule.severity === 'high' ? 'error' : rule.severity === 'medium' ? 'warning' : 'default'}
                    sx={{ mr: 1 }}
                  />
                )}

                {rule.applies_to_tasks && rule.applies_to_tasks.length > 0 && (
                  <Box mt={2}>
                    <Typography variant="caption" color="textSecondary">
                      Applied to tasks:
                    </Typography>
                    <Box display="flex" gap={1} mt={0.5}>
                      {rule.applies_to_tasks.map(task => (
                        <Chip
                          key={task}
                          label={task.replace(/_/g, ' ')}
                          size="small"
                          onDelete={() => removeRuleFromTask(selectedCategory, ruleId, task)}
                        />
                      ))}
                    </Box>
                  </Box>
                )}

                {rule.notes && (
                  <Typography variant="caption" display="block" sx={{ mt: 2, fontStyle: 'italic' }}>
                    Note: {rule.notes}
                  </Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Edit Rule Dialog */}
      <Dialog
        open={editDialog.open}
        onClose={closeEditDialog}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          {editDialog.ruleId && rules[editDialog.category]?.[editDialog.ruleId] 
            ? `Edit Rule: ${editDialog.rule?.name}`
            : 'Create New Rule'}
        </DialogTitle>
        <DialogContent>
          {editDialog.rule && (
            <Box sx={{ pt: 2 }}>
              <TextField
                fullWidth
                label="Rule Name"
                value={editDialog.rule.name || ''}
                onChange={(e) => updateEditRule('name', e.target.value)}
                margin="normal"
              />
              
              <TextField
                fullWidth
                label="Description"
                value={editDialog.rule.description || ''}
                onChange={(e) => updateEditRule('description', e.target.value)}
                margin="normal"
                multiline
                rows={2}
              />

              <FormControl fullWidth margin="normal">
                <InputLabel>Metric Type</InputLabel>
                <Select
                  value={editDialog.rule.metric_type || 'ratio'}
                  onChange={(e) => updateEditRule('metric_type', e.target.value)}
                  label="Metric Type"
                >
                  <MenuItem value="ratio">Ratio</MenuItem>
                  <MenuItem value="percentage">Percentage</MenuItem>
                  <MenuItem value="qualitative">Qualitative</MenuItem>
                </Select>
              </FormControl>

              {editDialog.category === 'red_flags' && (
                <>
                  <FormControl fullWidth margin="normal">
                    <InputLabel>Severity</InputLabel>
                    <Select
                      value={editDialog.rule.severity || 'medium'}
                      onChange={(e) => updateEditRule('severity', e.target.value)}
                      label="Severity"
                    >
                      <MenuItem value="low">Low</MenuItem>
                      <MenuItem value="medium">Medium</MenuItem>
                      <MenuItem value="high">High</MenuItem>
                    </Select>
                  </FormControl>

                  <TextField
                    fullWidth
                    label="Implication"
                    value={editDialog.rule.implication || ''}
                    onChange={(e) => updateEditRule('implication', e.target.value)}
                    margin="normal"
                    multiline
                    rows={2}
                  />
                </>
              )}

              {editDialog.rule.metric_type !== 'qualitative' && editDialog.category !== 'red_flags' && (
                <Box mt={3}>
                  <Typography variant="subtitle1" gutterBottom>
                    Thresholds
                  </Typography>
                  
                  <Box mb={2}>
                    <Typography variant="subtitle2" color="success.main">
                      Pass Threshold
                    </Typography>
                    <Grid container spacing={2}>
                      <Grid item xs={6}>
                        <FormControl fullWidth margin="normal">
                          <InputLabel>Operator</InputLabel>
                          <Select
                            value={editDialog.rule.thresholds?.pass?.operator || '<'}
                            onChange={(e) => updateThreshold('pass', 'operator', e.target.value)}
                            label="Operator"
                          >
                            <MenuItem value="<">Less than</MenuItem>
                            <MenuItem value=">">Greater than</MenuItem>
                          </Select>
                        </FormControl>
                      </Grid>
                      <Grid item xs={6}>
                        <TextField
                          fullWidth
                          label="Value"
                          type="number"
                          value={editDialog.rule.thresholds?.pass?.value || 0}
                          onChange={(e) => updateThreshold('pass', 'value', parseFloat(e.target.value))}
                          margin="normal"
                        />
                      </Grid>
                    </Grid>
                  </Box>

                  <Box mb={2}>
                    <Typography variant="subtitle2" color="warning.main">
                      Monitor Threshold
                    </Typography>
                    <Grid container spacing={2}>
                      <Grid item xs={6}>
                        <TextField
                          fullWidth
                          label="Min Value"
                          type="number"
                          value={editDialog.rule.thresholds?.monitor?.min || 0}
                          onChange={(e) => updateThreshold('monitor', 'min', parseFloat(e.target.value))}
                          margin="normal"
                        />
                      </Grid>
                      <Grid item xs={6}>
                        <TextField
                          fullWidth
                          label="Max Value"
                          type="number"
                          value={editDialog.rule.thresholds?.monitor?.max || 0}
                          onChange={(e) => updateThreshold('monitor', 'max', parseFloat(e.target.value))}
                          margin="normal"
                        />
                      </Grid>
                    </Grid>
                  </Box>

                  <Box mb={2}>
                    <Typography variant="subtitle2" color="error.main">
                      Fail Threshold
                    </Typography>
                    <Grid container spacing={2}>
                      <Grid item xs={6}>
                        <FormControl fullWidth margin="normal">
                          <InputLabel>Operator</InputLabel>
                          <Select
                            value={editDialog.rule.thresholds?.fail?.operator || '>'}
                            onChange={(e) => updateThreshold('fail', 'operator', e.target.value)}
                            label="Operator"
                          >
                            <MenuItem value="<">Less than</MenuItem>
                            <MenuItem value=">">Greater than</MenuItem>
                          </Select>
                        </FormControl>
                      </Grid>
                      <Grid item xs={6}>
                        <TextField
                          fullWidth
                          label="Value"
                          type="number"
                          value={editDialog.rule.thresholds?.fail?.value || 0}
                          onChange={(e) => updateThreshold('fail', 'value', parseFloat(e.target.value))}
                          margin="normal"
                        />
                      </Grid>
                    </Grid>
                  </Box>
                </Box>
              )}

              {editDialog.rule.metric_type === 'qualitative' && editDialog.category !== 'red_flags' && (
                <Box mt={3}>
                  <Typography variant="subtitle1" gutterBottom>
                    Qualitative Criteria
                  </Typography>
                  
                  <TextField
                    fullWidth
                    label="Pass Criteria"
                    value={editDialog.rule.thresholds?.pass?.criteria || ''}
                    onChange={(e) => updateThreshold('pass', 'criteria', e.target.value)}
                    margin="normal"
                    multiline
                    rows={2}
                  />
                  
                  <TextField
                    fullWidth
                    label="Monitor Criteria"
                    value={editDialog.rule.thresholds?.monitor?.criteria || ''}
                    onChange={(e) => updateThreshold('monitor', 'criteria', e.target.value)}
                    margin="normal"
                    multiline
                    rows={2}
                  />
                  
                  <TextField
                    fullWidth
                    label="Fail Criteria"
                    value={editDialog.rule.thresholds?.fail?.criteria || ''}
                    onChange={(e) => updateThreshold('fail', 'criteria', e.target.value)}
                    margin="normal"
                    multiline
                    rows={2}
                  />
                </Box>
              )}

              <TextField
                fullWidth
                label="Notes (Optional)"
                value={editDialog.rule.notes || ''}
                onChange={(e) => updateEditRule('notes', e.target.value)}
                margin="normal"
                multiline
                rows={2}
              />
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={closeEditDialog} startIcon={<Cancel />}>
            Cancel
          </Button>
          <Button onClick={saveRule} variant="contained" startIcon={<Save />}>
            Save
          </Button>
        </DialogActions>
      </Dialog>

      {/* Assign to Task Dialog */}
      <Dialog
        open={assignDialog.open}
        onClose={closeAssignDialog}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          Assign Rule to Task
        </DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="textSecondary" paragraph>
            Select a task to assign the rule "{assignDialog.rule?.name}" to:
          </Typography>
          <List>
            {Object.keys(tasks).map(taskName => {
              const isAssigned = assignDialog.rule?.applies_to_tasks?.includes(taskName)
              return (
                <ListItem 
                  key={taskName}
                  button={!isAssigned}
                  onClick={() => !isAssigned && assignRuleToTask(taskName)}
                  disabled={isAssigned}
                >
                  <ListItemText 
                    primary={taskName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    secondary={isAssigned ? 'Already assigned' : 'Click to assign'}
                  />
                  {isAssigned && (
                    <ListItemSecondaryAction>
                      <CheckCircle color="success" />
                    </ListItemSecondaryAction>
                  )}
                </ListItem>
              )
            })}
          </List>
        </DialogContent>
        <DialogActions>
          <Button onClick={closeAssignDialog}>
            Close
          </Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  )
}

export default RulesConfiguration