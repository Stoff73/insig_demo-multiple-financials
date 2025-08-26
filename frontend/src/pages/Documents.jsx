import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  Button,
  Alert,
  CircularProgress,
  LinearProgress,
  Divider,
  TextField,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Chip,
  Grid,
} from '@mui/material';
import {
  CloudUpload as UploadIcon,
  Refresh as RefreshIcon,
  ExpandMore as ExpandMoreIcon,
  Folder as FolderIcon,
  Business as BusinessIcon,
} from '@mui/icons-material';
import { fileAPI } from '../utils/api';
import { FILE_UPLOAD } from '../utils/constants';
import { SnackbarNotification } from '../components/common';
import FileList from '../components/FileList';
import useSnackbar from '../hooks/useSnackbar';
import useApi from '../hooks/useApi';

const Documents = () => {
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [converting, setConverting] = useState({});
  const [selectedTicker, setSelectedTicker] = useState('');
  const [expandedTickers, setExpandedTickers] = useState([]);
  const { snackbar, showSuccess, showError, closeSnackbar } = useSnackbar();
  
  const { 
    data: filesData, 
    loading, 
    execute: fetchFiles 
  } = useApi(fileAPI.getInputFiles);
  
  const filesByTicker = filesData?.filesByTicker || {};
  const tickers = Object.keys(filesByTicker).sort();

  useEffect(() => {
    fetchFiles();
  }, []);

  const handleToggleTicker = (ticker) => {
    setExpandedTickers(prev => 
      prev.includes(ticker) 
        ? prev.filter(t => t !== ticker)
        : [...prev, ticker]
    );
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    if (!selectedTicker) {
      showError('Please enter a ticker symbol before uploading');
      event.target.value = '';
      return;
    }

    setUploading(true);
    setUploadProgress(0);
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('ticker', selectedTicker.toUpperCase());

    try {
      // Simulate progress (since axios doesn't support upload progress in this config)
      const progressInterval = setInterval(() => {
        setUploadProgress((prev) => Math.min(prev + 10, 90));
      }, 100);

      const response = await fileAPI.uploadFile(formData, selectedTicker.toUpperCase());

      clearInterval(progressInterval);
      setUploadProgress(100);

      showSuccess(`Successfully uploaded: ${response.data.filename}`);
      
      // Refresh file list
      await fetchFiles();
      
      // Reset file input
      event.target.value = '';
    } catch (err) {
      showError(err.response?.data?.detail || err.message || 'Failed to upload file');
    } finally {
      setUploading(false);
      setUploadProgress(0);
    }
  };

  const handleDeleteFile = async (ticker, filename) => {
    if (!window.confirm(`Are you sure you want to delete ${filename} from ${ticker}?`)) {
      return;
    }

    try {
      await fileAPI.deleteFile(ticker, filename);
      showSuccess(`Successfully deleted: ${filename}`);
      await fetchFiles();
    } catch (err) {
      showError(err.response?.data?.detail || err.message || 'Failed to delete file');
    }
  };

  const handleConvertPDF = async (ticker, filename) => {
    const convertKey = `${ticker}/${filename}`;
    setConverting(prev => ({ ...prev, [convertKey]: true }));
    
    try {
      const response = await fileAPI.convertPDF(ticker, filename);
      showSuccess(`Successfully converted to: ${response.data.markdown_file}`);
      
      // Refresh file list to show new markdown file
      await fetchFiles();
    } catch (err) {
      showError(err.response?.data?.detail || err.message || 'Failed to convert PDF');
    } finally {
      setConverting(prev => {
        const newState = { ...prev };
        delete newState[convertKey];
        return newState;
      });
    }
  };


  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Document Management
      </Typography>
      
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="h6">
            Upload Documents
          </Typography>
          <Button
            startIcon={<RefreshIcon />}
            onClick={fetchFiles}
            disabled={loading}
          >
            Refresh
          </Button>
        </Box>
        
        <Alert severity="info" sx={{ mb: 2 }}>
          Upload financial documents for analysis. Supported formats: PDF, Markdown (.md), 
          Text (.txt), CSV, Excel (.xlsx), Word (.docx). 
          <br />
          <strong>PDF files can be converted to Markdown</strong> to preserve tables and financial data formatting.
          <br />
          Documents are organized by company ticker symbol (e.g., XPP, AAPL, MSFT).
        </Alert>

        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={4}>
            <TextField
              fullWidth
              label="Ticker Symbol"
              placeholder="e.g., XPP, AAPL"
              value={selectedTicker}
              onChange={(e) => setSelectedTicker(e.target.value.toUpperCase())}
              disabled={uploading}
              variant="outlined"
              size="small"
              InputProps={{
                startAdornment: <BusinessIcon sx={{ mr: 1, color: 'text.secondary' }} />,
              }}
            />
          </Grid>
          <Grid item xs={12} sm={8}>
            <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
              <input
                accept={FILE_UPLOAD.ACCEPTED_FORMATS}
                style={{ display: 'none' }}
                id="file-upload"
                type="file"
                onChange={handleFileUpload}
                disabled={uploading || !selectedTicker}
              />
              <label htmlFor="file-upload">
                <Button
                  variant="contained"
                  component="span"
                  startIcon={<UploadIcon />}
                  disabled={uploading || !selectedTicker}
                >
                  {uploading ? 'Uploading...' : 'Choose File'}
                </Button>
              </label>
              {!selectedTicker && (
                <Typography variant="caption" color="text.secondary">
                  Enter ticker first
                </Typography>
              )}
            </Box>
          </Grid>
        </Grid>

        {uploading && (
          <Box sx={{ mt: 2 }}>
            <LinearProgress variant="determinate" value={uploadProgress} />
            <Typography variant="caption" sx={{ mt: 1 }}>
              Uploading... {uploadProgress}%
            </Typography>
          </Box>
        )}
      </Paper>

      <Paper sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Documents by Company
          </Typography>
          <Chip 
            label={`${tickers.length} ${tickers.length === 1 ? 'Company' : 'Companies'}`}
            color="primary"
            size="small"
          />
        </Box>
        
        <Divider sx={{ mb: 2 }} />
        
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
            <CircularProgress />
          </Box>
        ) : tickers.length === 0 ? (
          <Typography color="textSecondary" sx={{ p: 2, textAlign: 'center' }}>
            No documents uploaded yet. Enter a ticker symbol and upload documents to analyze them.
          </Typography>
        ) : (
          <Box>
            {tickers.map((ticker) => {
              const tickerFiles = filesByTicker[ticker] || [];
              const fileCount = tickerFiles.length;
              const isExpanded = expandedTickers.includes(ticker);
              
              return (
                <Accordion 
                  key={ticker}
                  expanded={isExpanded}
                  onChange={() => handleToggleTicker(ticker)}
                  sx={{ mb: 1 }}
                >
                  <AccordionSummary
                    expandIcon={<ExpandMoreIcon />}
                    sx={{ 
                      backgroundColor: isExpanded ? 'action.hover' : 'background.paper',
                      '&:hover': { backgroundColor: 'action.hover' }
                    }}
                  >
                    <Box sx={{ display: 'flex', alignItems: 'center', width: '100%', gap: 2 }}>
                      <FolderIcon color="primary" />
                      <Typography variant="subtitle1" sx={{ fontWeight: 'medium' }}>
                        {ticker}
                      </Typography>
                      <Chip
                        label={`${fileCount} ${fileCount === 1 ? 'file' : 'files'}`}
                        size="small"
                        variant="outlined"
                      />
                    </Box>
                  </AccordionSummary>
                  <AccordionDetails sx={{ p: 0 }}>
                    <FileList
                      files={tickerFiles}
                      onDelete={(filename) => handleDeleteFile(ticker, filename)}
                      onConvert={(filename) => handleConvertPDF(ticker, filename)}
                      converting={Object.fromEntries(
                        Object.entries(converting)
                          .filter(([key]) => key.startsWith(`${ticker}/`))
                          .map(([key, value]) => [key.split('/')[1], value])
                      )}
                      showDivider={true}
                      dense={true}
                      emptyMessage={`No documents for ${ticker}`}
                    />
                  </AccordionDetails>
                </Accordion>
              );
            })}
          </Box>
        )}
      </Paper>

      <SnackbarNotification
        open={snackbar.open}
        message={snackbar.message}
        severity={snackbar.severity}
        onClose={closeSnackbar}
      />
    </Container>
  );
};

export default Documents;