// Common formatting utilities used across the application

/**
 * Format file size from bytes to human-readable format
 * @param {number} bytes - File size in bytes
 * @returns {string} Formatted file size
 */
export const formatFileSize = (bytes) => {
  if (!bytes || bytes === 0) return '0 B'
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

/**
 * Format date string to locale string
 * @param {string|Date} dateString - Date to format
 * @returns {string} Formatted date string
 */
export const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
}

/**
 * Format date to short format (date only)
 * @param {string|Date} dateString - Date to format
 * @returns {string} Formatted date string
 */
export const formatShortDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString()
}

/**
 * Group files by type/category
 * @param {Array} files - Array of file objects
 * @returns {Object} Files grouped by category
 */
export const groupFilesByType = (files) => {
  const groups = {
    'Primary Analysis': [],
    'Ownership Reports': [],
    'Earnings Quality': [],
    'Balance Sheet': [],
    'Investment Decisions': [],
    'Other': [],
  }

  files.forEach(file => {
    const name = file.name.toLowerCase()
    if (name.includes('primary') || name.includes('ratio')) {
      groups['Primary Analysis'].push(file)
    } else if (name.includes('ownership')) {
      groups['Ownership Reports'].push(file)
    } else if (name.includes('earning')) {
      groups['Earnings Quality'].push(file)
    } else if (name.includes('balance')) {
      groups['Balance Sheet'].push(file)
    } else if (name.includes('decision')) {
      groups['Investment Decisions'].push(file)
    } else {
      groups['Other'].push(file)
    }
  })

  return groups
}

/**
 * Get file extension from filename
 * @param {string} filename - File name
 * @returns {string} File extension
 */
export const getFileExtension = (filename) => {
  if (!filename) return ''
  const parts = filename.split('.')
  return parts.length > 1 ? parts.pop().toLowerCase() : ''
}