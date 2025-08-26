import React from 'react'
import {
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Box,
  Typography,
  Chip,
  CircularProgress,
  Divider
} from '@mui/material'
import {
  Visibility,
  Download,
  Delete,
  Transform as ConvertIcon
} from '@mui/icons-material'
import { FileIcon } from './common'
import { formatFileSize, formatDate } from '../utils/formatters'

/**
 * Reusable component for displaying file lists with actions
 */
function FileList({
  files = [],
  onView,
  onDownload,
  onDelete,
  onConvert,
  converting = {},
  showDivider = true,
  dense = false,
  getCategoryColor,
  getCategoryName,
  emptyMessage = 'No files available'
}) {
  if (!files || files.length === 0) {
    return (
      <Typography color="textSecondary" sx={{ p: 2, textAlign: 'center' }}>
        {emptyMessage}
      </Typography>
    )
  }

  return (
    <List dense={dense}>
      {files.map((file, index) => (
        <React.Fragment key={file.name || file.filename || index}>
          <ListItem>
            <Box sx={{ display: 'flex', alignItems: 'center', flex: 1 }}>
              <FileIcon filename={file.name || file.filename} sx={{ marginRight: 1 }} />
              <ListItemText
                primary={
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <span>{file.name || file.filename}</span>
                    {getCategoryName && (
                      <Chip
                        label={getCategoryName(file.name || file.filename)}
                        size="small"
                        color={getCategoryColor ? getCategoryColor(file.name || file.filename) : 'default'}
                      />
                    )}
                  </Box>
                }
                secondary={
                  file.size || file.modified ? (
                    <React.Fragment>
                      {file.size && formatFileSize(file.size)}
                      {file.size && file.modified && ' • '}
                      {file.modified && `Modified: ${formatDate(file.modified)}`}
                    </React.Fragment>
                  ) : null
                }
              />
            </Box>
            <ListItemSecondaryAction>
              <Box sx={{ display: 'flex', gap: 1 }}>
                {/* Convert PDF button */}
                {onConvert && (file.name || file.filename)?.toLowerCase().endsWith('.pdf') && (
                  <IconButton
                    edge="end"
                    aria-label="convert"
                    onClick={() => onConvert(file.name || file.filename)}
                    color="primary"
                    disabled={converting[file.name || file.filename]}
                    title="Convert to Markdown"
                    size={dense ? 'small' : 'medium'}
                  >
                    {converting[file.name || file.filename] ? (
                      <CircularProgress size={20} />
                    ) : (
                      <ConvertIcon fontSize={dense ? 'small' : 'medium'} />
                    )}
                  </IconButton>
                )}
                
                {/* View button for markdown files */}
                {onView && (file.name || file.filename)?.endsWith('.md') && (
                  <IconButton
                    edge="end"
                    aria-label="view"
                    onClick={() => onView(file)}
                    title="View"
                    size={dense ? 'small' : 'medium'}
                  >
                    <Visibility fontSize={dense ? 'small' : 'medium'} />
                  </IconButton>
                )}
                
                {/* Download button */}
                {onDownload && (
                  <IconButton
                    edge="end"
                    aria-label="download"
                    onClick={() => onDownload(file)}
                    title="Download"
                    size={dense ? 'small' : 'medium'}
                  >
                    <Download fontSize={dense ? 'small' : 'medium'} />
                  </IconButton>
                )}
                
                {/* Delete button */}
                {onDelete && (
                  <IconButton
                    edge="end"
                    aria-label="delete"
                    onClick={() => onDelete(file.name || file.filename)}
                    color="error"
                    title="Delete"
                    size={dense ? 'small' : 'medium'}
                  >
                    <Delete fontSize={dense ? 'small' : 'medium'} />
                  </IconButton>
                )}
              </Box>
            </ListItemSecondaryAction>
          </ListItem>
          {showDivider && index < files.length - 1 && <Divider />}
        </React.Fragment>
      ))}
    </List>
  )
}

export default FileList