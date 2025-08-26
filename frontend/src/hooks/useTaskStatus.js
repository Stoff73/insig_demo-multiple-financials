import { useState, useEffect, useCallback } from 'react'
import { analysisAPI } from '../utils/api'
import { POLLING_INTERVALS, TASK_STATUS } from '../utils/constants'
import usePolling from './usePolling'

/**
 * Hook for managing task status polling and state
 * @param {string} initialTaskId - Initial task ID to monitor
 * @returns {Object} - Task status management utilities
 */
export function useTaskStatus(initialTaskId = null) {
  const [currentTask, setCurrentTask] = useState(initialTaskId)
  const [taskStatus, setTaskStatus] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const fetchTaskStatus = useCallback(async () => {
    if (!currentTask) return
    
    try {
      const response = await analysisAPI.getStatus(currentTask)
      const status = response.data
      setTaskStatus(status)
      
      // Check if task is complete
      const isComplete = [
        TASK_STATUS.COMPLETED,
        TASK_STATUS.ERROR,
        'completed',
        'error',
        'partial_completion'
      ].includes(status.status)
      
      if (isComplete) {
        setCurrentTask(null)
        setLoading(false)
        return status
      }
    } catch (err) {
      console.error('Error fetching task status:', err)
      setError(err.message)
    }
  }, [currentTask])

  // Use polling hook
  usePolling(
    fetchTaskStatus,
    POLLING_INTERVALS.TASK_STATUS || 2000,
    !!currentTask,
    [currentTask]
  )

  const startTask = useCallback(async (taskId, initialStatus = null) => {
    setCurrentTask(taskId)
    setLoading(true)
    setError(null)
    
    if (initialStatus) {
      setTaskStatus(initialStatus)
    } else {
      setTaskStatus({
        task_id: taskId,
        status: TASK_STATUS.INITIALIZING || 'initializing',
        progress: 0,
        logs: ['Starting...']
      })
    }
  }, [])

  const stopTask = useCallback(() => {
    setCurrentTask(null)
    setLoading(false)
    setTaskStatus(null)
    setError(null)
  }, [])

  const reset = useCallback(() => {
    setCurrentTask(null)
    setTaskStatus(null)
    setLoading(false)
    setError(null)
  }, [])

  return {
    currentTask,
    taskStatus,
    loading,
    error,
    startTask,
    stopTask,
    reset,
    setTaskStatus,
    isRunning: !!currentTask && loading
  }
}

export default useTaskStatus