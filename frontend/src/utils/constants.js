// Application constants

// Task/Analysis status values
export const TASK_STATUS = {
  PENDING: 'pending',
  INITIALIZING: 'initializing',
  RUNNING: 'running',
  COMPLETED: 'completed',
  ERROR: 'error',
  PARTIAL_COMPLETION: 'partial_completion',
}

// Status colors for Material-UI chips
export const STATUS_COLORS = {
  [TASK_STATUS.COMPLETED]: 'success',
  [TASK_STATUS.ERROR]: 'error',
  [TASK_STATUS.RUNNING]: 'primary',
  [TASK_STATUS.PARTIAL_COMPLETION]: 'warning',
  default: 'default',
}

// File categories for grouping
export const FILE_CATEGORIES = {
  PRIMARY: 'Primary Analysis',
  OWNERSHIP: 'Ownership Reports',
  EARNINGS: 'Earnings Quality',
  BALANCE_SHEET: 'Balance Sheet',
  INVESTMENT: 'Investment Decisions',
  OTHER: 'Other',
}

// Ratio categories
export const RATIO_CATEGORIES = {
  valuation: 'Valuation',
  profitability: 'Profitability',
  liquidity: 'Liquidity',
  leverage: 'Leverage',
  efficiency: 'Efficiency',
  earnings_quality: 'Earnings Quality',
  asset_quality: 'Asset Quality',
  cash_flow: 'Cash Flow',
}

// Category order for display
export const CATEGORY_ORDER = [
  'valuation',
  'profitability',
  'liquidity',
  'leverage',
  'efficiency',
  'earnings_quality',
  'asset_quality',
  'cash_flow',
]

// Maximum number of companies for multi-company analysis
export const MAX_COMPANIES = 10

// Polling intervals (in milliseconds)
export const POLLING_INTERVALS = {
  TASK_STATUS: 2000,
  DASHBOARD_REFRESH: 5000,
}

// File upload settings
export const FILE_UPLOAD = {
  ACCEPTED_FORMATS: '.pdf,.md,.txt,.csv,.xlsx,.docx',
  MAX_SIZE: 50 * 1024 * 1024, // 50MB
}