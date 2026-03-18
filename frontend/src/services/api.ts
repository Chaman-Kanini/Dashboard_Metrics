import axios from 'axios';
import type { DashboardSummary, Session, Event, TimeSeriesData, HealthDistribution, Stats } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const dashboardApi = {
  getSummary: async (): Promise<DashboardSummary[]> => {
    const response = await api.get<DashboardSummary[]>('/dashboard/summary');
    return response.data;
  },

  getRecentSessions: async (limit = 50, source?: string): Promise<Session[]> => {
    const params = new URLSearchParams();
    params.append('limit', limit.toString());
    if (source) params.append('source', source);
    
    const response = await api.get<Session[]>(`/dashboard/sessions?${params}`);
    return response.data;
  },

  getSessionEvents: async (sessionId: string): Promise<Event[]> => {
    const response = await api.get<Event[]>(`/dashboard/sessions/${sessionId}/events`);
    return response.data;
  },

  getTimeSeries: async (days = 7): Promise<TimeSeriesData[]> => {
    const response = await api.get<TimeSeriesData[]>(`/dashboard/timeseries?days=${days}`);
    return response.data;
  },

  getHealthDistribution: async (): Promise<HealthDistribution[]> => {
    const response = await api.get<HealthDistribution[]>('/dashboard/health-distribution');
    return response.data;
  },

  getStats: async (): Promise<Stats> => {
    const response = await api.get<Stats>('/dashboard/stats');
    return response.data;
  },
};
