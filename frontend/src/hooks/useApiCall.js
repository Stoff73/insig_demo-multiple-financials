import { useState, useCallback } from 'react'

/**
 * Custom hook for API calls with loading, error, and data states
 * @param {Function} apiFunction - The API function to call
 * @returns {Object} Object containing data, loading, error states and execute function
 */
export const useApiCall = (apiFunction) => {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const execute = useCallback(async (...args) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await apiFunction(...args)
      setData(response.data)
      return response.data
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'An error occurred'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }, [apiFunction])

  const reset = useCallback(() => {
    setData(null)
    setError(null)
    setLoading(false)
  }, [])

  return { data, loading, error, execute, reset }
}

export default useApiCall