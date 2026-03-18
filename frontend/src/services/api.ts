import axios from 'axios';
import type { DashboardSummary, Session, Event, TimeSeriesData, HealthDistribution, Stats } from '../types';
import { transformKeys } from '../utils/transformers';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const dashboardApi = {
  getSummary: async (): Promise<DashboardSummary[]> => {
    const response = await api.get('/dashboard/summary');
    return transformKeys<DashboardSummary[]>(response.data);
  },

  getRecentSessions: async (limit = 50, source?: string): Promise<Session[]> => {
    const params = new URLSearchParams();
    params.append('limit', limit.toString());
    if (source) params.append('source', source);
    
    const response = await api.get(`/dashboard/sessions?${params}`);
    return transformKeys<Session[]>(response.data);
  },

  getSessionEvents: async (sessionId: string): Promise<Event[]> => {
    const response = await api.get(`/dashboard/sessions/${sessionId}/events`);
    return transformKeys<Event[]>(response.data);
  },

  getTimeSeries: async (days = 7): Promise<TimeSeriesData[]> => {
    const response = await api.get(`/dashboard/timeseries?days=${days}`);
    return transformKeys<TimeSeriesData[]>(response.data);
  },

  getHealthDistribution: async (): Promise<HealthDistribution[]> => {
    const response = await api.get('/dashboard/health-distribution');
    return transformKeys<HealthDistribution[]>(response.data);
  },

  getStats: async (): Promise<Stats> => {
    const response = await api.get('/dashboard/stats');
    return transformKeys<Stats>(response.data);
  },
};
