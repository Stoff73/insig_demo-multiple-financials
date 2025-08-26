import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Paper,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Alert,
  Breadcrumbs,
  Link,
} from '@mui/material'
import {
  Description,
  Folder,
  Archive,
  ExpandMore,
  NavigateNext,
} from '@mui/icons-material'
import { fileAPI, archiveAPI } from '../utils/api'
import MarkdownPreview from '../components/MarkdownPreview'
import useApi from '../hooks/useApi'

function CompanyReports() {
  const { ticker } = useParams()
  const navigate = useNavigate()
  const [selectedFile, setSelectedFile] = useState(null)
  const [fileContent, setFileContent] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  
  const { 
    data: outputData, 
    execute: fetchCompanyFiles 
  } = useApi(() => fileAPI.getCompanyOutputFiles(ticker))
  
  const { 
    data: archiveData, 
    execute: fetchCompanyArchives 
  } = useApi(() => archiveAPI.getCompanyArchives(ticker))
  
  const outputFiles = outputData?.files || []
  const archives = archiveData?.archives || []

  useEffect(() => {
    if (ticker) {
      fetchCompanyFiles()
      fetchCompanyArchives()
    }
  }, [ticker])

  const loadFile = async (filename, isArchive = false, timestamp = null) => {
    setLoading(true)
    setError(null)
    try {
      let url
      if (isArchive && timestamp) {
        url = `/api/archive/company/${ticker}/${timestamp}/${filename}`
      } else {
        url = `/api/files/output/company/${ticker}/${filename}`
      }
      
      const response = await fetch(url)
      const data = await response.text()
      setFileContent(data)
      setSelectedFile(filename)
    } catch (err) {
      setError('Failed to load file')
      console.error('Failed to load file:', err)
    } finally {
      setLoading(false)
    }
  }

  const getCategoryColor = (filename) => {
    if (filename.includes('primary') || filename.includes('ratios')) return 'primary'
    if (filename.includes('ownership')) return 'secondary'
    if (filename.includes('earning') || filename.includes('quality')) return 'warning'
    if (filename.includes('balance') || filename.includes('durability')) return 'info'
    if (filename.includes('decision')) return 'success'
    return 'default'
  }

  const getCategoryName = (filename) => {
    if (filename.includes('primary') || filename.includes('ratios')) return 'Primary Analysis'
    if (filename.includes('ownership')) return 'Ownership'
    if (filename.includes('earning') || filename.includes('quality')) return 'Earnings Quality'
    if (filename.includes('balance') || filename.includes('durability')) return 'Balance Sheet'
    if (filename.includes('decision')) return 'Decision'
    return 'Other'
  }

  return (
    <Box sx={{ p: 3 }}>
      <Breadcrumbs separator={<NavigateNext fontSize="small" />} sx={{ mb: 2 }}>
        <Link
          underline="hover"
          color="inherit"
          href="#"
          onClick={(e) => {
            e.preventDefault()
            navigate('/reports')
          }}
        >
          Reports
        </Link>
        <Typography color="text.primary">{ticker}</Typography>
      </Breadcrumbs>

      <Typography variant="h4" gutterBottom>
        {ticker} Company Reports
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* File List */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <Folder sx={{ mr: 1, verticalAlign: 'middle' }} />
                Current Analysis Files
              </Typography>
              
              {outputFiles.length === 0 ? (
                <Typography variant="body2" color="textSecondary">
                  No output files found for {ticker}
                </Typography>
              ) : (
                <List>
                  {outputFiles.map((file) => (
                    <ListItem key={file.name} disablePadding>
                      <ListItemButton
                        selected={selectedFile === file.name && !loading}
                        onClick={() => loadFile(file.name)}
                      >
                        <ListItemText
                          primary={
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <Description fontSize="small" />
                              <span>{file.name}</span>
                            </Box>
                          }
                          secondary={
                            <Box sx={{ mt: 0.5 }}>
                              <Chip
                                label={getCategoryName(file.name)}
                                size="small"
                                color={getCategoryColor(file.name)}
                              />
                            </Box>
                          }
                        />
                      </ListItemButton>
                    </ListItem>
                  ))}
                </List>
              )}
            </CardContent>
          </Card>

          {/* Archives */}
          <Card sx={{ mt: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <Archive sx={{ mr: 1, verticalAlign: 'middle' }} />
                Archived Analyses
              </Typography>
              
              {archives.length === 0 ? (
                <Typography variant="body2" color="textSecondary">
                  No archived analyses found
                </Typography>
              ) : (
                archives.map((archive) => (
                  <Accordion key={archive.timestamp}>
                    <AccordionSummary expandIcon={<ExpandMore />}>
                      <Typography variant="body2">
                        {new Date(archive.date).toLocaleString()}
                      </Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                      <List dense>
                        {archive.files.map((file) => (
                          <ListItem key={file.name} disablePadding>
                            <ListItemButton
                              onClick={() => loadFile(file.name, true, archive.timestamp)}
                            >
                              <ListItemText
                                primary={file.name}
                                secondary={
                                  <Chip
                                    label={getCategoryName(file.name)}
                                    size="small"
                                    color={getCategoryColor(file.name)}
                                  />
                                }
                              />
                            </ListItemButton>
                          </ListItem>
                        ))}
                      </List>
                    </AccordionDetails>
                  </Accordion>
                ))
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Content Viewer */}
        <Grid item xs={12} md={8}>
          <Card sx={{ height: '80vh', overflow: 'hidden' }}>
            <CardContent sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              {selectedFile ? (
                <>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                    <Typography variant="h6">
                      {selectedFile}
                    </Typography>
                    <Chip
                      label={getCategoryName(selectedFile)}
                      color={getCategoryColor(selectedFile)}
                    />
                  </Box>
                  
                  <Paper sx={{ flex: 1, overflow: 'auto', p: 2, bgcolor: 'grey.50' }}>
                    {loading ? (
                      <Typography>Loading...</Typography>
                    ) : (
                      <MarkdownPreview content={fileContent} />
                    )}
                  </Paper>
                </>
              ) : (
                <Box sx={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'center', 
                  height: '100%' 
                }}>
                  <Typography variant="body1" color="textSecondary">
                    Select a file to view its contents
                  </Typography>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  )
}

export default CompanyReports