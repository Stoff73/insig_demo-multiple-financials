import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  IconButton,
  Box,
  Typography,
  Paper
} from '@mui/material';
import {
  Close as CloseIcon,
  Fullscreen as FullscreenIcon,
  FullscreenExit as FullscreenExitIcon,
  Download as DownloadIcon
} from '@mui/icons-material';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const MarkdownPreview = ({ open, onClose, title, content, filename }) => {
  const [fullscreen, setFullscreen] = React.useState(false);

  const handleDownload = () => {
    const blob = new Blob([content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth={fullscreen ? false : 'lg'}
      fullWidth
      fullScreen={fullscreen}
      PaperProps={{
        sx: {
          height: fullscreen ? '100vh' : '80vh',
          display: 'flex',
          flexDirection: 'column'
        }
      }}
    >
      <DialogTitle sx={{ 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'space-between',
        borderBottom: 1,
        borderColor: 'divider'
      }}>
        <Typography variant="h6" component="div">
          {title || filename}
        </Typography>
        <Box>
          <IconButton
            onClick={() => setFullscreen(!fullscreen)}
            size="small"
            sx={{ mr: 1 }}
          >
            {fullscreen ? <FullscreenExitIcon /> : <FullscreenIcon />}
          </IconButton>
          <IconButton
            onClick={handleDownload}
            size="small"
            sx={{ mr: 1 }}
          >
            <DownloadIcon />
          </IconButton>
          <IconButton
            onClick={onClose}
            size="small"
          >
            <CloseIcon />
          </IconButton>
        </Box>
      </DialogTitle>
      
      <DialogContent sx={{ 
        flex: 1, 
        overflow: 'auto',
        p: 3,
        backgroundColor: '#fafafa'
      }}>
        <Paper 
          elevation={0}
          sx={{ 
            p: 4,
            backgroundColor: 'white',
            minHeight: '100%',
            '& .markdown-body': {
              fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif',
              lineHeight: 1.6,
              '& h1': {
                fontSize: '2em',
                fontWeight: 600,
                marginBottom: '16px',
                marginTop: '24px',
                paddingBottom: '0.3em',
                borderBottom: '1px solid #e1e4e8',
              },
              '& h2': {
                fontSize: '1.5em',
                fontWeight: 600,
                marginBottom: '16px',
                marginTop: '24px',
                paddingBottom: '0.3em',
                borderBottom: '1px solid #e1e4e8',
              },
              '& h3': {
                fontSize: '1.25em',
                fontWeight: 600,
                marginBottom: '16px',
                marginTop: '24px',
              },
              '& h4': {
                fontSize: '1em',
                fontWeight: 600,
                marginBottom: '16px',
                marginTop: '24px',
              },
              '& p': {
                marginBottom: '16px',
                marginTop: 0,
              },
              '& ul, & ol': {
                paddingLeft: '2em',
                marginBottom: '16px',
                marginTop: 0,
              },
              '& li': {
                marginBottom: '0.25em',
              },
              '& hr': {
                height: '0.25em',
                padding: 0,
                margin: '24px 0',
                backgroundColor: '#e1e4e8',
                border: 0,
              },
              '& blockquote': {
                padding: '0 1em',
                color: '#6a737d',
                borderLeft: '0.25em solid #dfe2e5',
                margin: '0 0 16px 0',
              },
              '& code': {
                padding: '0.2em 0.4em',
                margin: 0,
                fontSize: '85%',
                backgroundColor: 'rgba(27,31,35,0.05)',
                borderRadius: '3px',
                fontFamily: 'SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace',
              },
              '& pre': {
                padding: '16px',
                overflow: 'auto',
                fontSize: '85%',
                lineHeight: 1.45,
                backgroundColor: '#f6f8fa',
                borderRadius: '3px',
                marginBottom: '16px',
                '& code': {
                  padding: 0,
                  margin: 0,
                  backgroundColor: 'transparent',
                  fontSize: '100%',
                },
              },
              '& table': {
                width: '100%',
                borderCollapse: 'collapse',
                marginBottom: '16px',
                display: 'block',
                overflow: 'auto',
              },
              '& table th': {
                fontWeight: 600,
                padding: '6px 13px',
                border: '1px solid #dfe2e5',
                backgroundColor: '#f6f8fa',
                textAlign: 'left',
              },
              '& table td': {
                padding: '6px 13px',
                border: '1px solid #dfe2e5',
              },
              '& table tr': {
                backgroundColor: 'white',
                borderTop: '1px solid #c6cbd1',
              },
              '& table tr:nth-of-type(2n)': {
                backgroundColor: '#f6f8fa',
              },
              '& table td[align="right"], & table th[align="right"]': {
                textAlign: 'right',
              },
              '& table td[align="center"], & table th[align="center"]': {
                textAlign: 'center',
              },
              '& img': {
                maxWidth: '100%',
                boxSizing: 'content-box',
              },
              '& a': {
                color: '#0366d6',
                textDecoration: 'none',
                '&:hover': {
                  textDecoration: 'underline',
                },
              },
            }
          }}
        >
          <Box className="markdown-body">
            <ReactMarkdown 
              remarkPlugins={[remarkGfm]}
              components={{
                // Custom table rendering for better financial data display
                table: ({node, ...props}) => (
                  <div style={{ overflowX: 'auto', marginBottom: '16px' }}>
                    <table {...props} style={{ minWidth: '100%' }} />
                  </div>
                ),
                // Preserve HTML comments (like page markers)
                p: ({node, children, ...props}) => {
                  const text = String(children);
                  if (text.startsWith('<!-- ') && text.endsWith(' -->')) {
                    return (
                      <div style={{ 
                        color: '#6a737d', 
                        fontSize: '0.875em',
                        fontStyle: 'italic',
                        margin: '8px 0'
                      }}>
                        {text.replace('<!-- ', '').replace(' -->', '')}
                      </div>
                    );
                  }
                  return <p {...props}>{children}</p>;
                }
              }}
            >
              {content}
            </ReactMarkdown>
          </Box>
        </Paper>
      </DialogContent>
      
      <DialogActions sx={{ borderTop: 1, borderColor: 'divider', px: 3, py: 2 }}>
        <Button onClick={onClose} variant="contained">
          Close
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default MarkdownPreview;