import axios from 'axios'

// API base URL - can be configured via environment variable
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for common handling
api.interceptors.request.use(
  (config) => {
    // Add any auth tokens or common headers here if needed
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle common errors here
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// File Management APIs
export const fileAPI = {
  getInputFiles: () => api.get('/api/files/input'),
  getOutputFiles: () => api.get('/api/files/output'),
  getOutputFile: (filename) => api.get(`/api/files/output/${filename}`),
  uploadFile: (formData, ticker) => {
    // Add ticker to formData if not already present
    if (ticker && !formData.has('ticker')) {
      formData.append('ticker', ticker);
    }
    return api.post('/api/files/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  uploadCompanyFile: (ticker, formData) => api.post(`/api/files/upload/${ticker}`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  deleteFile: (ticker, filename) => api.delete(`/api/files/${ticker}/${encodeURIComponent(filename)}`),
  convertPDF: (ticker, filename) => api.post(`/api/files/convert/${ticker}/${encodeURIComponent(filename)}`),
  getCompanyOutputFiles: (ticker) => api.get(`/api/files/output/company/${ticker}`),
}

// Analysis APIs
export const analysisAPI = {
  startSingle: (data) => api.post('/api/analysis/start', data),
  startMulti: (data) => api.post('/api/analysis/start-multi', data),
  getStatus: (taskId) => api.get(`/api/analysis/status/${taskId}`),
  listTasks: () => api.get('/api/analysis/list'),
  stopAnalysis: (taskId) => api.delete(`/api/analysis/stop/${taskId}`),
}

// Configuration APIs
export const configAPI = {
  getAgents: () => api.get('/api/config/agents'),
  updateAgents: (data) => api.put('/api/config/agents', data),
  getTasks: () => api.get('/api/config/tasks'),
  updateTasks: (data) => api.put('/api/config/tasks', data),
}

// Rules APIs
export const rulesAPI = {
  getRules: () => api.get('/api/rules'),
  createRule: (data) => api.post('/api/rules', data),
  updateRule: (id, data) => api.put(`/api/rules/${id}`, data),
  deleteRule: (id) => api.delete(`/api/rules/${id}`),
}

// Ratios APIs
export const ratiosAPI = {
  getRatios: (ticker) => api.get(`/api/ratios/${ticker}`),
  updateRatios: (ticker, data) => api.put(`/api/ratios/${ticker}`, data),
  getEnabledRatios: (ticker) => api.get(`/api/ratios/${ticker}/enabled`),
  enableRatio: (ticker, category, ratioKey) => api.post(`/api/ratios/${ticker}/${category}/${ratioKey}/enable`),
  disableRatio: (ticker, category, ratioKey) => api.post(`/api/ratios/${ticker}/${category}/${ratioKey}/disable`),
}

// Archive APIs
export const archiveAPI = {
  getArchives: () => api.get('/api/archive'),
  getArchivedFile: (pathOrTimestamp, filename = null) => {
    // Support both path format (ticker/timestamp/filename) and legacy format
    if (filename) {
      return api.get(`/api/archive/${pathOrTimestamp}/${filename}`)
    } else {
      return api.get(`/api/archive/${pathOrTimestamp}`)
    }
  },
  getCompanyArchives: (ticker) => api.get(`/api/archive/company/${ticker}`),
}

// Company APIs
export const companyAPI = {
  listCompanies: () => api.get('/api/companies/list'),
  getCompanyStatus: (ticker) => api.get(`/api/companies/${ticker}/status`),
}

export default api