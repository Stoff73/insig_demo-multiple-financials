import React from 'react'
import {
  Description,
  PictureAsPdf,
  TableChart,
  Article,
} from '@mui/icons-material'
import { getFileExtension } from '../../utils/formatters'

/**
 * Reusable file icon component based on file extension
 * @param {string} filename - File name
 * @param {Object} props - Additional props for the icon
 */
const FileIcon = ({ filename, ...props }) => {
  const ext = getFileExtension(filename)
  
  switch (ext) {
    case 'pdf':
      return <PictureAsPdf color="error" {...props} />
    case 'md':
      return <Article color="primary" {...props} />
    case 'xlsx':
    case 'csv':
      return <TableChart color="success" {...props} />
    case 'docx':
    case 'txt':
      return <Description color="info" {...props} />
    default:
      return <Description {...props} />
  }
}

export default FileIcon