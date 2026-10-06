import { Destination, DestinationDetail, Trip, User } from '../types';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';

export const api = {
  // Destinations
  async getDestinations(query?: string, travelType?: string, interest?: string): Promise<Destination[]> {
    const params = new URLSearchParams();
    if (query) params.append('query', query);
    if (travelType) params.append('travel_type', travelType);
    if (interest) params.append('interest', interest);
    
    const res = await fetch(`${BASE_URL}/destinations?${params.toString()}`);
    const data = await res.json();
    return data.success ? data.data : [];
  },

  async getDestination(id: number): Promise<DestinationDetail | null> {
    const res = await fetch(`${BASE_URL}/destinations/${id}`);
    const data = await res.json();
    return data.success ? data.data : null;
  },

  // Trips
  async generateTrip(payload: {
    destination_id: number;
    travel_type: string;
    num_travellers: number;
    duration_days: number;
    start_date?: string;
    end_date?: string;
    budget_tier: string;
    interests: string[];
    pace_preference: string;
    additional_notes?: string;
  }): Promise<Trip | null> {
    const token = localStorage.getItem('travenza_token');
    const headers: Record<string, string> = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const res = await fetch(`${BASE_URL}/trips/generate`, {
      method: 'POST',
      headers,
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    return data.success ? data.data : null;
  },

  async getTrip(id: number): Promise<Trip | null> {
    const res = await fetch(`${BASE_URL}/trips/${id}`);
    const data = await res.json();
    return data.success ? data.data : null;
  },

  async getSavedTrips(): Promise<any[]> {
    const token = localStorage.getItem('travenza_token');
    const headers: Record<string, string> = {};
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const res = await fetch(`${BASE_URL}/saved-trips`, { headers });
    const data = await res.json();
    return data.success ? data.data : [];
  },

  async deleteTrip(id: number): Promise<boolean> {
    const res = await fetch(`${BASE_URL}/trips/${id}`, { method: 'DELETE' });
    const data = await res.json();
    return data.success;
  },

  // Auth
  async login(email: string, password: string): Promise<{ user: User; token: string } | null> {
    const res = await fetch(`${BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    const data = await res.json();
    if (data.success) {
      localStorage.setItem('travenza_token', data.data.access_token);
      return { user: data.data.user, token: data.data.access_token };
    }
    return null;
  },

  async register(email: string, password: string, full_name?: string): Promise<{ user: User; token: string } | null> {
    const res = await fetch(`${BASE_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, full_name }),
    });
    const data = await res.json();
    if (data.success) {
      localStorage.setItem('travenza_token', data.data.access_token);
      return { user: data.data.user, token: data.data.access_token };
    }
    return null;
  },

  async getMe(): Promise<User | null> {
    const token = localStorage.getItem('travenza_token');
    if (!token) return null;
    try {
      const res = await fetch(`${BASE_URL}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      return data.success ? data.data : null;
    } catch {
      return null;
    }
  }
};
