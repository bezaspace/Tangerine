import { useState, useEffect } from 'react';
import { practitionersApi } from '../services/practitioners';
import { Practitioner, PractitionerResponse } from '../types/practitioner';

interface UsePractitionersState {
  practitioners: Practitioner[];
  loading: boolean;
  error: string | null;
  total: number;
}

export const usePractitioners = (params?: {
  specialty?: string;
  location?: string;
  limit?: number;
}) => {
  const [state, setState] = useState<UsePractitionersState>({
    practitioners: [],
    loading: true,
    error: null,
    total: 0,
  });

  const fetchPractitioners = async () => {
    try {
      setState(prev => ({ ...prev, loading: true, error: null }));
      const response = await practitionersApi.getAllPractitioners(params);
      setState({
        practitioners: response.practitioners,
        loading: false,
        error: null,
        total: response.total,
      });
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'Failed to fetch practitioners',
      }));
    }
  };

  useEffect(() => {
    fetchPractitioners();
  }, [params?.specialty, params?.location, params?.limit]);

  const refetch = () => {
    fetchPractitioners();
  };

  return {
    ...state,
    refetch,
  };
};

export const usePractitioner = (id: number) => {
  const [state, setState] = useState<{
    practitioner: Practitioner | null;
    loading: boolean;
    error: string | null;
  }>({
    practitioner: null,
    loading: true,
    error: null,
  });

  const fetchPractitioner = async () => {
    try {
      setState(prev => ({ ...prev, loading: true, error: null }));
      const practitioner = await practitionersApi.getPractitionerById(id);
      setState({
        practitioner,
        loading: false,
        error: null,
      });
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'Failed to fetch practitioner',
      }));
    }
  };

  useEffect(() => {
    if (id) {
      fetchPractitioner();
    }
  }, [id]);

  const refetch = () => {
    fetchPractitioner();
  };

  return {
    ...state,
    refetch,
  };
};