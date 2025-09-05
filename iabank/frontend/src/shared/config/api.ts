/**
 * API configuration - Foundation DNA for frontend API communication.
 * 
 * This module establishes the base configuration for all API communication,
 * following the established patterns for the IABANK frontend architecture.
 */

export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  TIMEOUT: 10000,
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000,
} as const

export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login/',
    REFRESH: '/auth/refresh/',
    VERIFY: '/auth/verify/',
  },
  USERS: {
    LIST: '/users/',
    PROFILE: '/users/profile/',
    UPDATE_PROFILE: '/users/update_profile/',
    CHANGE_PASSWORD: '/users/change_password/',
  },
  CUSTOMERS: {
    LIST: '/customers/',
    SEARCH: '/customers/search/',
    ACTIVE: '/customers/active/',
    STATS: '/customers/stats/',
  },
  HEALTH: {
    CHECK: '/health/',
    READY: '/health/ready/',
  },
} as const