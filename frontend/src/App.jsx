import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import ErrorBoundary from './components/ErrorBoundary'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Analysis from './pages/Analysis'
import MultiCompanyAnalysis from './pages/MultiCompanyAnalysis'
import Reports from './pages/Reports'
import CompanyReports from './pages/CompanyReports'
import Configuration from './pages/Configuration'
import RatiosConfiguration from './pages/RatiosConfiguration'
import Documents from './pages/Documents'
import { CompanyProvider } from './contexts/CompanyContext'

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
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
                <Route path="/multi-analysis" element={<MultiCompanyAnalysis />} />
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