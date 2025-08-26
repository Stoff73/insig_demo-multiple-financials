import { useState, useCallback } from 'react'

/**
 * Generic API hook for handling loading, error states and API calls
 * @param {Function} apiFunction - The API function to call
 * @returns {Object} - { data, loading, error, execute, reset }
 */
export function useApi(apiFunction) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const execute = useCallback(async (...args) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await apiFunction(...args)
      const result = response.data
      setData(result)
      return result
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

  return {
    data,
    loading,
    error,
    execute,
    reset,
    setData,
    setError
  }
}

export default useApi