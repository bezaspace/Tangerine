export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  originalPrice?: number;
  rating: number;
  reviews: number;
  image: string;
  category: string;
  inStock: boolean;
}

export interface ProductResponse {
  products: Product[];
  total: number;
}

export interface ProductCategory {
  name: string;
  count: number;
}

export interface ApiError {
  message: string;
  status: number;
}