import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import ErrorBoundary from './components/ErrorBoundary'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Analysis from './pages/Analysis'
import Reports from './pages/Reports'
import CompanyReports from './pages/CompanyReports'
import Configuration from './pages/Configuration'
import RatiosConfiguration from './pages/RatiosConfiguration'
import Documents from './pages/Documents'
import { CompanyProvider } from './contexts/CompanyContext'

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#0A2540',  // Deep navy blue
      light: '#1E3A5F',
      dark: '#051429',
    },
    secondary: {
      main: '#00D4FF',  // Bright cyan accent
      light: '#5BE5FF',
      dark: '#00A7CC',
    },
    background: {
      default: '#FAFBFC',
      paper: '#FFFFFF',
    },
    text: {
      primary: '#0A2540',
      secondary: '#5E6C84',
    },
    success: {
      main: '#00C48C',
      light: '#33D3A4',
      dark: '#009C6E',
    },
    error: {
      main: '#FF5630',
      light: '#FF7856',
      dark: '#CC4526',
    },
    warning: {
      main: '#FFAB00',
      light: '#FFBC33',
      dark: '#CC8900',
    },
    info: {
      main: '#0065FF',
      light: '#3384FF',
      dark: '#0051CC',
    },
  },
  typography: {
    fontFamily: '"Inter", "Helvetica Neue", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 700,
      letterSpacing: '-0.02em',
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
      letterSpacing: '-0.01em',
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 600,
      letterSpacing: '-0.01em',
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 600,
      letterSpacing: '-0.01em',
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 600,
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 600,
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.6,
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.6,
    },
    button: {
      textTransform: 'none',
      fontWeight: 500,
    },
  },
  shape: {
    borderRadius: 0,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 4,
          padding: '10px 20px',
          transition: 'all 0.3s ease',
          '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: '0 8px 16px rgba(10, 37, 64, 0.15)',
          },
        },
        contained: {
          boxShadow: '0 4px 12px rgba(10, 37, 64, 0.08)',
          '&:hover': {
            boxShadow: '0 8px 20px rgba(10, 37, 64, 0.12)',
          },
        },
        containedSecondary: {
          color: '#0A2540',
          '&:hover': {
            backgroundColor: '#00C4ED',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          boxShadow: '0 4px 12px rgba(10, 37, 64, 0.08)',
          transition: 'all 0.3s ease',
          '&:hover': {
            boxShadow: '0 12px 24px rgba(10, 37, 64, 0.12)',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          boxShadow: '0 2px 8px rgba(10, 37, 64, 0.06)',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          boxShadow: 'none',
          background: 'linear-gradient(135deg, #0A2540 0%, #1E3A5F 100%)',
          borderRadius: 0,
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          background: 'linear-gradient(180deg, #0A2540 0%, #051429 100%)',
          color: '#FFFFFF',
          borderRadius: 0,
          border: 'none',
        },
      },
    },
    MuiListItemButton: {
      styleOverrides: {
        root: {
          margin: '2px 0',
          borderRadius: 0,
          transition: 'all 0.3s ease',
          '&:hover': {
            backgroundColor: 'rgba(0, 212, 255, 0.1)',
          },
          '&.Mui-selected': {
            backgroundColor: 'rgba(0, 212, 255, 0.15)',
            borderLeft: '4px solid #00D4FF',
            '&:hover': {
              backgroundColor: 'rgba(0, 212, 255, 0.2)',
            },
          },
        },
      },
    },
    MuiListItemIcon: {
      styleOverrides: {
        root: {
          color: '#00D4FF',
          minWidth: 44,
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 4,
          fontWeight: 500,
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 4,
            transition: 'all 0.3s ease',
            '&:hover': {
              '& .MuiOutlinedInput-notchedOutline': {
                borderColor: '#00D4FF',
              },
            },
            '&.Mui-focused': {
              '& .MuiOutlinedInput-notchedOutline': {
                borderColor: '#00D4FF',
                borderWidth: 2,
              },
            },
          },
        },
      },
    },
    MuiTableHead: {
      styleOverrides: {
        root: {
          '& .MuiTableCell-head': {
            backgroundColor: '#F6F8FA',
            fontWeight: 600,
            color: '#0A2540',
          },
        },
      },
    },
    MuiTableRow: {
      styleOverrides: {
        root: {
          transition: 'all 0.2s ease',
          '&:hover': {
            backgroundColor: '#F6F8FA',
          },
        },
      },
    },
    MuiAlert: {
      styleOverrides: {
        root: {
          borderRadius: 4,
        },
      },
    },
    MuiLinearProgress: {
      styleOverrides: {
        root: {
          borderRadius: 4,
          height: 6,
        },
      },
    },
  },
})

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <CompanyProvider>
          <Router>
            <Layout>
              <Routes>
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/documents" element={<Documents />} />
                <Route path="/analysis" element={<Analysis />} />
                <Route path="/reports" element={<Reports />} />
                <Route path="/reports/company/:ticker" element={<CompanyReports />} />
                <Route path="/configuration" element={<Configuration />} />
                <Route path="/ratios" element={<RatiosConfiguration />} />
              </Routes>
            </Layout>
          </Router>
        </CompanyProvider>
      </ThemeProvider>
    </ErrorBoundary>
  )
}

export default App