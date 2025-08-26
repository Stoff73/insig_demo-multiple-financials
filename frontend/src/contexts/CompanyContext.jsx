import React, { createContext, useContext, useState, useEffect } from 'react'

const CompanyContext = createContext()

export const useCompany = () => {
  const context = useContext(CompanyContext)
  if (!context) {
    throw new Error('useCompany must be used within CompanyProvider')
  }
  return context
}

export const CompanyProvider = ({ children }) => {
  // Initialize from localStorage if available
  const [company, setCompanyState] = useState(() => {
    return localStorage.getItem('selectedCompany') || ''
  })
  
  const [ticker, setTickerState] = useState(() => {
    return localStorage.getItem('selectedTicker') || ''
  })

  // Wrapper functions to update both state and localStorage
  const setCompany = (value) => {
    setCompanyState(value)
    if (value) {
      localStorage.setItem('selectedCompany', value)
    } else {
      localStorage.removeItem('selectedCompany')
    }
  }

  const setTicker = (value) => {
    // Always uppercase ticker symbols
    const upperValue = value ? value.toUpperCase() : ''
    setTickerState(upperValue)
    if (upperValue) {
      localStorage.setItem('selectedTicker', upperValue)
    } else {
      localStorage.removeItem('selectedTicker')
    }
  }

  // Clear both company and ticker
  const clearCompanyData = () => {
    setCompany('')
    setTicker('')
  }

  // Listen for storage events to sync across tabs/windows
  useEffect(() => {
    const handleStorageChange = (e) => {
      if (e.key === 'selectedCompany') {
        setCompanyState(e.newValue || '')
      } else if (e.key === 'selectedTicker') {
        setTickerState(e.newValue || '')
      }
    }

    window.addEventListener('storage', handleStorageChange)
    return () => window.removeEventListener('storage', handleStorageChange)
  }, [])

  const value = {
    company,
    ticker,
    setCompany,
    setTicker,
    clearCompanyData,
  }

  return (
    <CompanyContext.Provider value={value}>
      {children}
    </CompanyContext.Provider>
  )
}