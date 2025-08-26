import { useEffect, useRef } from 'react'

/**
 * Custom hook for polling with automatic cleanup
 * @param {Function} callback - Function to call on each interval
 * @param {number} interval - Polling interval in milliseconds
 * @param {boolean} enabled - Whether polling is enabled
 * @param {Array} deps - Dependencies array for the effect
 */
export const usePolling = (callback, interval, enabled = true, deps = []) => {
  const savedCallback = useRef()

  // Remember the latest callback
  useEffect(() => {
    savedCallback.current = callback
  }, [callback])

  // Set up the interval
  useEffect(() => {
    if (!enabled) return

    const tick = () => {
      if (savedCallback.current) {
        savedCallback.current()
      }
    }

    // Call immediately on mount if enabled
    tick()

    const id = setInterval(tick, interval)
    return () => clearInterval(id)
  }, [interval, enabled, ...deps])
}

export default usePolling