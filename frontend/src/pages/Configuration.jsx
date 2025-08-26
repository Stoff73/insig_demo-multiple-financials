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
} from '@mui/material'
import {
  Person,
  Assignment,
  Psychology,
  Edit,
  Save,
  Cancel,
  Add,
  Delete,
} from '@mui/icons-material'
import axios from 'axios'

function TabPanel({ children, value, index }) {
  return (
    <div hidden={value !== index}>
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  )
}

function Configuration() {
  const [tabValue, setTabValue] = useState(0)
  const [agents, setAgents] = useState(null)
  const [tasks, setTasks] = useState(null)
  const [loading, setLoading] = useState(true)
  const [editDialog, setEditDialog] = useState({ open: false, type: null, key: null, data: null })
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' })

  useEffect(() => {
    fetchConfigurations()
  }, [])

  const fetchConfigurations = async () => {
    try {
      const [agentsRes, tasksRes] = await Promise.all([
        axios.get('/api/config/agents'),
        axios.get('/api/config/tasks'),
      ])
      setAgents(agentsRes.data)
      setTasks(tasksRes.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching configurations:', error)
      setLoading(false)
      setSnackbar({ open: true, message: 'Failed to load configurations', severity: 'error' })
    }
  }

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue)
  }

  const openEditDialog = (type, key, data) => {
    setEditDialog({ open: true, type, key, data: JSON.parse(JSON.stringify(data)) })
  }

  const closeEditDialog = () => {
    setEditDialog({ open: false, type: null, key: null, data: null })
  }

  const saveConfiguration = async () => {
    try {
      if (editDialog.type === 'agent') {
        const updatedAgents = { ...agents, [editDialog.key]: editDialog.data }
        await axios.put('/api/config/agents', updatedAgents)
        setAgents(updatedAgents)
        setSnackbar({ open: true, message: 'Agent configuration updated successfully', severity: 'success' })
      } else if (editDialog.type === 'task') {
        const updatedTasks = { ...tasks, [editDialog.key]: editDialog.data }
        await axios.put('/api/config/tasks', updatedTasks)
        setTasks(updatedTasks)
        setSnackbar({ open: true, message: 'Task configuration updated successfully', severity: 'success' })
      }
      closeEditDialog()
    } catch (error) {
      console.error('Error saving configuration:', error)
      setSnackbar({ open: true, message: 'Failed to save configuration', severity: 'error' })
    }
  }

  const updateEditData = (field, value) => {
    setEditDialog(prev => ({
      ...prev,
      data: { ...prev.data, [field]: value }
    }))
  }

  const addNewAgent = () => {
    const newKey = `agent_${Date.now()}`
    const newAgent = {
      role: 'New Agent',
      goal: 'Define the goal for this agent',
      backstory: 'Define the backstory for this agent',
      max_iter: 3
    }
    openEditDialog('agent', newKey, newAgent)
  }

  const addNewTask = () => {
    const newKey = `task_${Date.now()}`
    const newTask = {
      description: 'Define the task description',
      expected_output: 'Define the expected output',
      agent: Object.keys(agents || {})[0] || 'victoria_clarke',
      output_file: `output/${newKey}.md`
    }
    openEditDialog('task', newKey, newTask)
  }

  const deleteItem = async (type, key) => {
    if (!window.confirm(`Are you sure you want to delete this ${type}?`)) return
    
    try {
      if (type === 'agent') {
        const updatedAgents = { ...agents }
        delete updatedAgents[key]
        await axios.put('/api/config/agents', updatedAgents)
        setAgents(updatedAgents)
        setSnackbar({ open: true, message: 'Agent deleted successfully', severity: 'success' })
      } else if (type === 'task') {
        const updatedTasks = { ...tasks }
        delete updatedTasks[key]
        await axios.put('/api/config/tasks', updatedTasks)
        setTasks(updatedTasks)
        setSnackbar({ open: true, message: 'Task deleted successfully', severity: 'success' })
      }
    } catch (error) {
      console.error('Error deleting item:', error)
      showError('Failed to delete item')
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
        Configuration
      </Typography>
      
      <Paper sx={{ width: '100%' }}>
        <Tabs value={tabValue} onChange={handleTabChange}>
          <Tab label="Agents" icon={<Person />} iconPosition="start" />
          <Tab label="Tasks" icon={<Assignment />} iconPosition="start" />
        </Tabs>
        
        <TabPanel value={tabValue} index={0}>
          <Box display="flex" justifyContent="flex-end" mb={2}>
            <Button
              variant="contained"
              startIcon={<Add />}
              onClick={addNewAgent}
            >
              Add New Agent
            </Button>
          </Box>
          
          <Grid container spacing={3}>
            {agents && Object.entries(agents).map(([key, agent]) => (
              <Grid item xs={12} md={6} key={key}>
                <Card>
                  <CardContent>
                    <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
                      <Box display="flex" alignItems="center">
                        <Psychology color="primary" sx={{ mr: 1 }} />
                        <Typography variant="h6">
                          {agent.role}
                        </Typography>
                      </Box>
                      <Box>
                        <IconButton
                          size="small"
                          onClick={() => openEditDialog('agent', key, agent)}
                        >
                          <Edit />
                        </IconButton>
                        <IconButton
                          size="small"
                          color="error"
                          onClick={() => deleteItem('agent', key)}
                        >
                          <Delete />
                        </IconButton>
                      </Box>
                    </Box>
                    
                    <Typography variant="body2" color="textSecondary" paragraph>
                      {agent.goal}
                    </Typography>
                    
                    <Typography variant="caption" display="block" sx={{ mt: 2 }}>
                      <strong>Backstory:</strong> {agent.backstory?.substring(0, 150)}...
                    </Typography>
                    
                    {agent.max_iter && (
                      <Chip 
                        label={`Max iterations: ${agent.max_iter}`} 
                        size="small" 
                        sx={{ mt: 2 }}
                      />
                    )}
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </TabPanel>
        
        <TabPanel value={tabValue} index={1}>
          <Box display="flex" justifyContent="flex-end" mb={2}>
            <Button
              variant="contained"
              startIcon={<Add />}
              onClick={addNewTask}
            >
              Add New Task
            </Button>
          </Box>
          
          <Grid container spacing={3}>
            {tasks && Object.entries(tasks).map(([key, task]) => (
              <Grid item xs={12} key={key}>
                <Card>
                  <CardContent>
                    <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
                      <Box display="flex" alignItems="center">
                        <Assignment color="primary" sx={{ mr: 1 }} />
                        <Typography variant="h6">
                          {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                        </Typography>
                      </Box>
                      <Box>
                        <IconButton
                          size="small"
                          onClick={() => openEditDialog('task', key, task)}
                        >
                          <Edit />
                        </IconButton>
                        <IconButton
                          size="small"
                          color="error"
                          onClick={() => deleteItem('task', key)}
                        >
                          <Delete />
                        </IconButton>
                      </Box>
                    </Box>
                    
                    <Typography variant="body2" color="textSecondary" paragraph>
                      {task.description}
                    </Typography>
                    
                    <Box display="flex" gap={1} mt={2}>
                      {task.agent && (
                        <Chip 
                          label={`Agent: ${task.agent}`} 
                          size="small"
                          color="primary"
                          variant="outlined"
                        />
                      )}
                      {task.output_file && (
                        <Chip 
                          label={`Output: ${task.output_file}`} 
                          size="small"
                          color="secondary"
                          variant="outlined"
                        />
                      )}
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </TabPanel>
      </Paper>

      {/* Edit Dialog */}
      <Dialog
        open={editDialog.open}
        onClose={closeEditDialog}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Edit {editDialog.type === 'agent' ? 'Agent' : 'Task'}: {editDialog.key}
        </DialogTitle>
        <DialogContent>
          {editDialog.data && (
            <Box sx={{ pt: 2 }}>
              {editDialog.type === 'agent' ? (
                <>
                  <TextField
                    fullWidth
                    label="Role"
                    value={editDialog.data.role || ''}
                    onChange={(e) => updateEditData('role', e.target.value)}
                    margin="normal"
                  />
                  <TextField
                    fullWidth
                    label="Goal"
                    value={editDialog.data.goal || ''}
                    onChange={(e) => updateEditData('goal', e.target.value)}
                    margin="normal"
                    multiline
                    rows={2}
                  />
                  <TextField
                    fullWidth
                    label="Backstory"
                    value={editDialog.data.backstory || ''}
                    onChange={(e) => updateEditData('backstory', e.target.value)}
                    margin="normal"
                    multiline
                    rows={4}
                  />
                  <TextField
                    fullWidth
                    label="Max Iterations"
                    type="number"
                    value={editDialog.data.max_iter || 3}
                    onChange={(e) => updateEditData('max_iter', parseInt(e.target.value))}
                    margin="normal"
                  />
                </>
              ) : (
                <>
                  <TextField
                    fullWidth
                    label="Description"
                    value={editDialog.data.description || ''}
                    onChange={(e) => updateEditData('description', e.target.value)}
                    margin="normal"
                    multiline
                    rows={3}
                  />
                  <TextField
                    fullWidth
                    label="Expected Output"
                    value={editDialog.data.expected_output || ''}
                    onChange={(e) => updateEditData('expected_output', e.target.value)}
                    margin="normal"
                    multiline
                    rows={3}
                  />
                  <TextField
                    fullWidth
                    label="Agent"
                    value={editDialog.data.agent || ''}
                    onChange={(e) => updateEditData('agent', e.target.value)}
                    margin="normal"
                    select
                    SelectProps={{ native: true }}
                  >
                    {agents && Object.keys(agents).map(key => (
                      <option key={key} value={key}>{key}</option>
                    ))}
                  </TextField>
                  <TextField
                    fullWidth
                    label="Output File"
                    value={editDialog.data.output_file || ''}
                    onChange={(e) => updateEditData('output_file', e.target.value)}
                    margin="normal"
                  />
                </>
              )}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={closeEditDialog} startIcon={<Cancel />}>
            Cancel
          </Button>
          <Button onClick={saveConfiguration} variant="contained" startIcon={<Save />}>
            Save
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

export default Configuration