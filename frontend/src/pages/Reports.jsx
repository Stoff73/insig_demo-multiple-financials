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
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Chip,
  Alert,
} from '@mui/material'
import {
  Description,
  ExpandMore,
  Archive as ArchiveIcon,
  NewReleases,
  Folder,
} from '@mui/icons-material'
import { fileAPI, archiveAPI } from '../utils/api'
import { formatDate, groupFilesByType } from '../utils/formatters'
import { EmptyState } from '../components/common'
import FileList from '../components/FileList'
import MarkdownPreview from '../components/MarkdownPreview'
import useApi from '../hooks/useApi'

function TabPanel({ children, value, index }) {
  return (
    <div hidden={value !== index}>
      {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
    </div>
  )
}

function Reports() {
  const [tabValue, setTabValue] = useState(0)
  const [selectedFile, setSelectedFile] = useState(null)
  const [fileContent, setFileContent] = useState('')
  const [openPreview, setOpenPreview] = useState(false)
  
  const { data: outputData, execute: fetchOutputFiles } = useApi(fileAPI.getOutputFiles)
  const { data: archiveData, execute: fetchArchives } = useApi(archiveAPI.getArchives)
  
  const outputFiles = outputData?.files || []
  const archives = archiveData?.archives || []
  const loading = !outputData && !archiveData

  useEffect(() => {
    fetchOutputFiles()
    fetchArchives()
  }, [])

  const viewFile = async (file, isArchive = false, timestamp = null, archivePath = null) => {
    const filename = file.name || file.filename || file
    const filePath = file.path || filename  // Use path if available
    try {
      let response
      if (isArchive && archivePath) {
        response = await archiveAPI.getArchivedFile(`${archivePath}/${filename}`)
      } else if (isArchive && timestamp) {
        response = await archiveAPI.getArchivedFile(timestamp, filename)
      } else {
        response = await fileAPI.getOutputFile(filePath)
      }
      setFileContent(response.data)
      setSelectedFile(filename)
      setOpenPreview(true)
    } catch (error) {
      console.error('Error viewing file:', error)
    }
  }

  const downloadFile = (file, isArchive = false, timestamp = null, archivePath = null) => {
    const filename = file.name || file.filename || file
    const filePath = file.path || filename  // Use path if available
    if (isArchive && archivePath) {
      window.open(`/api/archive/${archivePath}/${filename}`, '_blank')
    } else if (isArchive && timestamp) {
      window.open(`/api/archive/${timestamp}/${filename}`, '_blank')
    } else {
      window.open(`/api/files/output/${filePath}`, '_blank')
    }
  }


  const handleTabChange = (event, newValue) => {
    setTabValue(newValue)
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Reports
      </Typography>
      
      <Paper sx={{ width: '100%' }}>
        <Tabs value={tabValue} onChange={handleTabChange}>
          <Tab 
            label="Latest Analysis" 
            icon={<NewReleases />} 
            iconPosition="start"
          />
          <Tab 
            label="Archive" 
            icon={<ArchiveIcon />} 
            iconPosition="start"
          />
        </Tabs>
        
        <TabPanel value={tabValue} index={0}>
          {outputFiles.length > 0 ? (
            <>
              <Alert severity="info" sx={{ mb: 3 }}>
                Showing reports from the latest analysis. Previous analyses are available in the Archive tab.
              </Alert>
              
              <Grid container spacing={3}>
                {Object.entries(groupFilesByType(outputFiles)).map(([category, files]) => (
                  files.length > 0 && (
                    <Grid item xs={12} md={6} key={category}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            {category}
                            <Chip 
                              label={files.length} 
                              size="small" 
                              sx={{ ml: 1 }}
                              color="primary"
                            />
                          </Typography>
                          
                          <FileList
                            files={files}
                            onView={viewFile}
                            onDownload={downloadFile}
                            showDivider={false}
                          />
                        </CardContent>
                      </Card>
                    </Grid>
                  )
                ))}
              </Grid>
            </>
          ) : (
            <EmptyState
              icon={<Description />}
              title="No current reports available"
              subtitle="Run an analysis to generate new reports"
            />
          )}
        </TabPanel>
        
        <TabPanel value={tabValue} index={1}>
          {archives.length > 0 ? (
            <>
              <Alert severity="info" sx={{ mb: 3 }}>
                Browse historical analyses. Each archive contains all reports from a single analysis run.
              </Alert>
              
              {archives.map((archive) => (
                <Accordion key={archive.timestamp}>
                  <AccordionSummary expandIcon={<ExpandMore />}>
                    <Box display="flex" alignItems="center" width="100%">
                      <Folder color="action" sx={{ mr: 2 }} />
                      <Typography sx={{ flexGrow: 1 }}>
                        Analysis from {formatDate(archive.date)}
                      </Typography>
                      <Chip 
                        label={`${archive.file_count} files`} 
                        size="small"
                        sx={{ mr: 2 }}
                      />
                    </Box>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Grid container spacing={2}>
                      {Object.entries(groupFilesByType(archive.files)).map(([category, files]) => (
                        files.length > 0 && (
                          <Grid item xs={12} md={6} key={category}>
                            <Typography variant="subtitle2" gutterBottom>
                              {category}
                            </Typography>
                            <FileList
                              files={files}
                              onView={(file) => viewFile(file, true, archive.timestamp, archive.path)}
                              onDownload={(file) => downloadFile(file, true, archive.timestamp, archive.path)}
                              dense={true}
                              showDivider={false}
                            />
                          </Grid>
                        )
                      ))}
                    </Grid>
                  </AccordionDetails>
                </Accordion>
              ))}
            </>
          ) : (
            <EmptyState
              icon={<ArchiveIcon />}
              title="No archived reports"
              subtitle="Archives will appear here after running multiple analyses"
            />
          )}
        </TabPanel>
      </Paper>

      {/* Markdown Preview */}
      <MarkdownPreview
        open={openPreview}
        onClose={() => setOpenPreview(false)}
        title={selectedFile}
        content={fileContent}
        filename={selectedFile}
      />
    </Box>
  )
}

export default Reports