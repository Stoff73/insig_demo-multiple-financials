import React, { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import {
  AppBar,
  Box,
  Drawer,
  IconButton,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  Avatar,
} from '@mui/material'
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  Analytics as AnalyticsIcon,
  Description as DescriptionIcon,
  Settings as SettingsIcon,
  Folder as FolderIcon,
  Calculate as CalculateIcon,
  AutoAwesome,
} from '@mui/icons-material'

const drawerWidth = 260

const menuItems = [
  { text: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
  { text: 'Documents', icon: <FolderIcon />, path: '/documents' },
  { text: 'Analysis', icon: <AnalyticsIcon />, path: '/analysis' },
  { text: 'Reports', icon: <DescriptionIcon />, path: '/reports' },
  { text: 'Configuration', icon: <SettingsIcon />, path: '/configuration' },
  { text: 'Ratios', icon: <CalculateIcon />, path: '/ratios' },
]

function Layout({ children }) {
  const [mobileOpen, setMobileOpen] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen)
  }

  const drawer = (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Toolbar sx={{ 
        py: 2, 
        px: 2,
        background: 'transparent',
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        minHeight: 64,
      }}>
        <Box sx={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: 1.5,
          width: '100%'
        }}>
          <Avatar sx={{ 
            width: 36, 
            height: 36,
            background: 'linear-gradient(135deg, #00D4FF 0%, #0065FF 100%)',
            borderRadius: 1,
          }}>
            <AutoAwesome sx={{ fontSize: 20 }} />
          </Avatar>
          <Box>
            <Typography 
              variant="h6" 
              sx={{ 
                fontWeight: 700,
                color: '#FFFFFF',
                letterSpacing: '0.02em'
              }}
            >
              INSIG AI
            </Typography>
            <Typography 
              variant="caption" 
              sx={{ 
                color: '#00D4FF',
                fontSize: '0.7rem',
                letterSpacing: '0.05em'
              }}
            >
              FINANCIAL ANALYSIS
            </Typography>
          </Box>
        </Box>
      </Toolbar>
      <List sx={{ px: 0, py: 2, flexGrow: 1 }}>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              selected={location.pathname === item.path}
              onClick={() => navigate(item.path)}
              sx={{
                color: location.pathname === item.path ? '#FFFFFF' : 'rgba(255, 255, 255, 0.7)',
                px: 3,
                py: 1.5,
                '&:hover': {
                  color: '#FFFFFF',
                },
              }}
            >
              <ListItemIcon sx={{ 
                color: location.pathname === item.path ? '#00D4FF' : 'rgba(255, 255, 255, 0.5)' 
              }}>
                {item.icon}
              </ListItemIcon>
              <ListItemText 
                primary={item.text}
                primaryTypographyProps={{
                  fontSize: '0.95rem',
                  fontWeight: location.pathname === item.path ? 600 : 400,
                }}
              />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      <Box sx={{ 
        p: 2, 
        borderTop: '1px solid rgba(255, 255, 255, 0.1)',
        color: 'rgba(255, 255, 255, 0.5)',
        fontSize: '0.75rem',
        textAlign: 'center'
      }}>
        <Typography variant="caption" sx={{ color: 'inherit' }}>
          Powered by AI
        </Typography>
      </Box>
    </Box>
  )

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar
        position="fixed"
        elevation={0}
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
          borderBottom: 'none',
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, flexGrow: 1 }}>
            <Typography 
              variant="h6" 
              noWrap 
              component="div"
              sx={{ 
                fontWeight: 600,
                background: 'linear-gradient(135deg, #FFFFFF 0%, #00D4FF 100%)',
                backgroundClip: 'text',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
              }}
            >
              Intelligent Financial Analysis Platform
            </Typography>
          </Box>
        </Toolbar>
      </AppBar>
      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true,
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { 
              boxSizing: 'border-box', 
              width: drawerWidth,
              borderRadius: 0,
            },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { 
              boxSizing: 'border-box', 
              width: drawerWidth,
              borderRight: 'none',
            },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          mt: 8,
          minHeight: 'calc(100vh - 64px)',
          background: 'linear-gradient(180deg, #FAFBFC 0%, #F0F4F8 100%)',
        }}
      >
        {children}
      </Box>
    </Box>
  )
}

export default Layout