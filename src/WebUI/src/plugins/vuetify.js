import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

export default createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: { mdi },
  },
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        dark: false,
        colors: {
          // Primary brand colors - Modern purple gradient
          primary: '#1E40AF', // Blue-800 - represents trust, reliability, authority
          'primary-lighten-1': '#3B82F6', // Blue-500
          'primary-lighten-2': '#60A5FA', // Blue-400
          'primary-darken-1': '#1E3A8A', // Blue-900
          'primary-darken-2': '#1E1B4B', // Indigo-900
          
          // Secondary colors - Alert/Warning (Amber/Orange for misinformation)
          secondary: '#EA580C', // Orange-600 - represents caution, fact-checking alerts
          'secondary-lighten-1': '#FB923C', // Orange-400
          'secondary-darken-1': '#C2410C', // Orange-700
          
          // Accent colors - Vibrant teal
          accent: '#06B6D4', // Cyan-500
          'accent-lighten-1': '#22D3EE', // Cyan-400
          'accent-darken-1': '#0891B2', // Cyan-600
          
          // Semantic colors
          success: '#10B981', // Emerald-500
          'success-lighten-1': '#34D399', // Emerald-400
          'success-lighten-2': '#6EE7B7', // Emerald-300
          'success-lighten-3': '#A7F3D0', // Emerald-200
          warning: '#F59E0B', // Amber-500
          'warning-lighten-1': '#FBBF24', // Amber-400
          error: '#EF4444', // Red-500
          'error-lighten-1': '#F87171', // Red-400
          'error-lighten-2': '#FCA5A5', // Red-300
          'error-lighten-3': '#FEE2E2', // Red-200
          info: '#3B82F6', // Blue-500
          'info-lighten-1': '#60A5FA', // Blue-400
          
          // Background colors
          background: '#FEFEFE', // Pure white with slight warmth
          surface: '#FFFFFF',
          'surface-variant': '#F8FAFC', // Slate-50
          'surface-bright': '#FFFFFF',
          'surface-light': '#EEEEEE',
          'surface-dark': '#424242',
          
          // Text colors
          'on-primary': '#FFFFFF',
          'on-secondary': '#FFFFFF',
          'on-accent': '#FFFFFF',
          'on-success': '#FFFFFF',
          'on-warning': '#000000',
          'on-error': '#FFFFFF',
          'on-info': '#FFFFFF',
          'on-background': '#1E293B', // Slate-800
          'on-surface': '#1E293B', // Slate-800
          'on-surface-variant': '#64748B', // Slate-500
          
          // Additional custom colors
          'primary-container': '#E0E7FF', // Indigo-100
          'secondary-container': '#FCE7F3', // Pink-100
          'accent-container': '#CFFAFE', // Cyan-100
          outline: '#CBD5E1', // Slate-300
          'outline-variant': '#E2E8F0', // Slate-200
        },
      },
      dark: {
        dark: true,
        colors: {
           // Primary brand colors - Brighter blue for dark mode (trust)
           primary: '#60A5FA', // Blue-400
           'primary-lighten-1': '#93C5FD', // Blue-300
           'primary-lighten-2': '#BFDBFE', // Blue-200
           'primary-darken-1': '#3B82F6', // Blue-500
           'primary-darken-2': '#2563EB', // Blue-600
           
           // Secondary colors - Brighter orange for dark mode (alert)
           secondary: '#FB923C', // Orange-400
           'secondary-lighten-1': '#FDBA74', // Orange-300
           'secondary-darken-1': '#EA580C', // Orange-600
          
          // Accent colors
          accent: '#22D3EE', // Cyan-400
          'accent-lighten-1': '#67E8F9', // Cyan-300
          'accent-darken-1': '#06B6D4', // Cyan-500
          
          // Semantic colors
          success: '#6EE7B7', // Emerald-300
          'success-lighten-1': '#34D399', // Emerald-400
          'success-lighten-2': '#10B981', // Emerald-500
          'success-lighten-3': '#059669', // Emerald-600
          warning: '#FBBF24', // Amber-400
          'warning-lighten-1': '#FCD34D', // Amber-300
          error: '#FCA5A5', // Red-300
          'error-lighten-1': '#F87171', // Red-400
          'error-lighten-2': '#EF4444', // Red-500
          'error-lighten-3': '#DC2626', // Red-600
          info: '#60A5FA', // Blue-400
          'info-lighten-1': '#93C5FD', // Blue-300
          
          // Background colors - Rich dark palette
          background: '#0F172A', // Slate-900
          surface: '#1E293B', // Slate-800
          'surface-variant': '#334155', // Slate-700
          'surface-bright': '#475569', // Slate-600
          'surface-light': '#64748B', // Slate-500
          'surface-dark': '#0F172A', // Slate-900
          
          // Text colors
          'on-primary': '#000000',
          'on-secondary': '#000000',
          'on-accent': '#000000',
          'on-success': '#000000',
          'on-warning': '#000000',
          'on-error': '#000000',
          'on-info': '#000000',
          'on-background': '#F1F5F9', // Slate-100
          'on-surface': '#F1F5F9', // Slate-100
          'on-surface-variant': '#CBD5E1', // Slate-300
          
          // Additional custom colors
          'primary-container': '#312E81', // Indigo-900
          'secondary-container': '#831843', // Pink-900
          'accent-container': '#164E63', // Cyan-900
          outline: '#475569', // Slate-600
          'outline-variant': '#334155', // Slate-700
        },
      },
    },
  },
  display: {
    mobileBreakpoint: 'sm',
    thresholds: {
      xs: 0,
      sm: 600,
      md: 960,
      lg: 1264,
      xl: 1904,
    },
  },
  defaults: {
    // Beautiful default styling for components
    VBtn: {
      style: {
        textTransform: 'none', // Remove uppercase
        fontWeight: '500',
        letterSpacing: '0.025em',
      },
      rounded: 'lg',
      elevation: 2,
    },
    VCard: {
      elevation: 4,
      rounded: 'xl',
    },
    VSheet: {
      rounded: 'lg',
    },
    VTextField: {
      variant: 'outlined',
      density: 'comfortable',
      rounded: 'lg',
    },
    VTextarea: {
      variant: 'outlined',
      density: 'comfortable',
      rounded: 'lg',
    },
    VSelect: {
      variant: 'outlined',
      density: 'comfortable',
      rounded: 'lg',
    },
    VAutocomplete: {
      variant: 'outlined',
      density: 'comfortable',
      rounded: 'lg',
    },
    VChip: {
      rounded: 'pill',
      elevation: 1,
    },
    VDialog: {
      rounded: 'xl',
    },
    VAppBar: {
      elevation: 2,
    },
    VNavigationDrawer: {
      elevation: 4,
    },
    VFab: {
      elevation: 6,
    },
    VMenu: {
      rounded: 'lg',
      elevation: 8,
    },
    VTooltip: {
      rounded: 'lg',
    },
    VSnackbar: {
      rounded: 'lg',
      elevation: 6,
    },
    VAlert: {
      rounded: 'lg',
      elevation: 2,
    },
    VProgressCircular: {
      width: 4,
    },
    VProgressLinear: {
      rounded: true,
      height: 6,
    },
    VSlider: {
      thumbSize: 20,
      trackSize: 6,
      rounded: true,
    },
    VSwitch: {
      inset: true,
    },
    VCheckbox: {
      density: 'comfortable',
    },
    VRadio: {
      density: 'comfortable',
    },
    VTabs: {
      height: 56,
    },
    VTab: {
      style: {
        textTransform: 'none',
        fontWeight: '500',
        letterSpacing: '0.025em',
      },
    },
    VExpansionPanels: {
      style: {
        borderRadius: '12px !important',
      },
    },
    VExpansionPanel: {
      style: {
        borderRadius: '12px !important',
      },
    },
  },
})