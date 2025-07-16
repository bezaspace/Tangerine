import { api } from './api';
import { Practitioner, PractitionerResponse } from '../types/practitioner';

export const practitionersApi = {
  // Get all practitioners
  getAllPractitioners: async (params?: {
    specialty?: string;
    location?: string;
    limit?: number;
  }): Promise<PractitionerResponse> => {
    const response = await api.get('/api/practitioners', { params });
    return response.data;
  },

  // Get practitioner by ID
  getPractitionerById: async (id: number): Promise<Practitioner> => {
    const response = await api.get(`/api/practitioners/${id}`);
    return response.data;
  },

  // Search practitioners
  searchPractitioners: async (query: string, limit?: number): Promise<PractitionerResponse> => {
    const response = await api.get('/api/practitioners/search', {
      params: { q: query, limit }
    });
    return response.data;
  },

  // Health check
  healthCheck: async (): Promise<{ status: string; service: string }> => {
    const response = await api.get('/health');
    return response.data;
  }
};