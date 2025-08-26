import React from 'react'
import { Box, Typography, Button, Paper } from '@mui/material'
import { ErrorOutline, Refresh } from '@mui/icons-material'

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo)
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null })
    window.location.reload()
  }

  render() {
    if (this.state.hasError) {
      return (
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            minHeight: '100vh',
            p: 3
          }}
        >
          <Paper sx={{ p: 4, maxWidth: 600, textAlign: 'center' }}>
            <ErrorOutline sx={{ fontSize: 60, color: 'error.main', mb: 2 }} />
            <Typography variant="h5" gutterBottom>
              Something went wrong
            </Typography>
            <Typography variant="body1" color="textSecondary" sx={{ mb: 3 }}>
              An unexpected error occurred. Please try refreshing the page.
            </Typography>
            {this.state.error && (
              <Typography 
                variant="body2" 
                sx={{ 
                  mb: 3, 
                  p: 2, 
                  bgcolor: 'grey.100', 
                  borderRadius: 1,
                  fontFamily: 'monospace',
                  fontSize: '0.875rem'
                }}
              >
                {this.state.error.toString()}
              </Typography>
            )}
            <Button
              variant="contained"
              startIcon={<Refresh />}
              onClick={this.handleReset}
            >
              Refresh Page
            </Button>
          </Paper>
        </Box>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary