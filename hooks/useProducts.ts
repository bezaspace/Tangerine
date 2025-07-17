import { useState, useEffect } from 'react';
import { productsApi } from '../services/api';
import { Product, ProductResponse, ProductCategory } from '../types/product';

interface UseProductsState {
  products: Product[];
  loading: boolean;
  error: string | null;
  total: number;
}

export const useProducts = (params?: {
  category?: string;
  query?: string;
  inStockOnly?: boolean;
  limit?: number;
}) => {
  const [state, setState] = useState<UseProductsState>({
    products: [],
    loading: true,
    error: null,
    total: 0,
  });

  const fetchProducts = async () => {
    try {
      setState(prev => ({ ...prev, loading: true, error: null }));
      const response = await productsApi.getAllProducts(params);
      setState({
        products: response.products,
        loading: false,
        error: null,
        total: response.total,
      });
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'Failed to fetch products',
      }));
    }
  };

  useEffect(() => {
    fetchProducts();
  }, [params?.category, params?.query, params?.inStockOnly, params?.limit]);

  const refetch = () => {
    fetchProducts();
  };

  return {
    ...state,
    refetch,
  };
};

export const useProduct = (id: number) => {
  const [state, setState] = useState<{
    product: Product | null;
    loading: boolean;
    error: string | null;
  }>({
    product: null,
    loading: true,
    error: null,
  });

  const fetchProduct = async () => {
    try {
      setState(prev => ({ ...prev, loading: true, error: null }));
      const product = await productsApi.getProductById(id);
      setState({
        product,
        loading: false,
        error: null,
      });
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'Failed to fetch product',
      }));
    }
  };

  useEffect(() => {
    if (id) {
      fetchProduct();
    }
  }, [id]);

  const refetch = () => {
    fetchProduct();
  };

  return {
    ...state,
    refetch,
  };
};

export const useProductCategories = () => {
  const [state, setState] = useState<{
    categories: ProductCategory[];
    loading: boolean;
    error: string | null;
  }>({
    categories: [],
    loading: true,
    error: null,
  });

  const fetchCategories = async () => {
    try {
      setState(prev => ({ ...prev, loading: true, error: null }));
      const categories = await productsApi.getCategories();
      setState({
        categories,
        loading: false,
        error: null,
      });
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'Failed to fetch categories',
      }));
    }
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  const refetch = () => {
    fetchCategories();
  };

  return {
    ...state,
    refetch,
  };
};

export const useProductSearch = () => {
  const [state, setState] = useState<UseProductsState>({
    products: [],
    loading: false,
    error: null,
    total: 0,
  });

  const searchProducts = async (
    query: string,
    category?: string,
    inStockOnly?: boolean,
    limit?: number
  ) => {
    try {
      setState(prev => ({ ...prev, loading: true, error: null }));
      const response = await productsApi.searchProducts(query, category, inStockOnly, limit);
      setState({
        products: response.products,
        loading: false,
        error: null,
        total: response.total,
      });
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'Failed to search products',
      }));
    }
  };

  const clearSearch = () => {
    setState({
      products: [],
      loading: false,
      error: null,
      total: 0,
    });
  };

  return {
    ...state,
    searchProducts,
    clearSearch,
  };
};