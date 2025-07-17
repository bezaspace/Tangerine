import axios from 'axios';

// API base URL - using your local IP address for development
const API_BASE_URL = 'http://192.168.1.40:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    if (__DEV__) {
      console.log('API Request:', config.method?.toUpperCase(), config.url);
    }
    return config;
  },
  (error) => {
    if (__DEV__) {
      console.error('API Request Error:', error);
    }
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    if (__DEV__) {
      console.log('API Response:', response.status, response.config.url);
    }
    return response;
  },
  (error) => {
    if (__DEV__) {
      console.error('API Response Error:', error.response?.status, error.message);
    }
    
    // Handle common errors
    if (error.response?.status === 404) {
      throw new Error('Resource not found');
    } else if (error.response?.status >= 500) {
      throw new Error('Server error. Please try again later.');
    } else if (error.code === 'NETWORK_ERROR' || error.message === 'Network Error') {
      throw new Error('Network error. Please check your connection.');
    }
    
    throw error;
  }
);

// Product API functions
import { Product, ProductResponse, ProductCategory } from '../types/product';

export const productsApi = {
  // Get all products
  getAllProducts: async (params?: {
    category?: string;
    query?: string;
    inStockOnly?: boolean;
    limit?: number;
  }): Promise<ProductResponse> => {
    const response = await api.get('/api/products', { 
      params: {
        category: params?.category,
        query: params?.query,
        in_stock_only: params?.inStockOnly,
        limit: params?.limit
      }
    });
    return response.data;
  },

  // Get product by ID
  getProductById: async (id: number): Promise<Product> => {
    const response = await api.get(`/api/products/${id}`);
    return response.data;
  },

  // Search products
  searchProducts: async (
    query: string, 
    category?: string, 
    inStockOnly?: boolean, 
    limit?: number
  ): Promise<ProductResponse> => {
    const response = await api.get('/api/products/search', {
      params: { 
        q: query, 
        category,
        in_stock_only: inStockOnly,
        limit 
      }
    });
    return response.data;
  },

  // Get categories
  getCategories: async (): Promise<ProductCategory[]> => {
    const response = await api.get('/api/categories');
    return response.data;
  }
};

export default api;