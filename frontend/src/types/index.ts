export interface Destination {
  id: number;
  name: string;
  country_name: string;
  currency: string;
  tagline: string;
  description?: string;
  hero_image: string;
  thumbnail: string;
  approx_daily_budget: number;
  best_time_to_visit: string;
  is_featured: boolean;
  trending_score: number;
  interests: string[];
  travel_types: string[];
}

export interface Attraction {
  id: number;
  name: string;
  category: string;
  description: string;
  estimated_duration_hours: number;
  estimated_cost: number;
  best_time_of_day?: string;
  location_area?: string;
}

export interface LocalService {
  id: number;
  category: string;
  name: string;
  purpose: string;
  platform: string;
  app_link?: string;
  explanation: string;
  recommended: boolean;
}

export interface CultureGuide {
  id: number;
  category: string;
  title: string;
  description: string;
  importance_level: string;
}

export interface SafetyInfo {
  id: number;
  title: string;
  category: string;
  description: string;
  severity: string;
}

export interface EmergencyContact {
  id: number;
  service_type: string;
  contact_number: string;
  notes?: string;
}

export interface DestinationDetail extends Destination {
  attractions: Attraction[];
  local_services: LocalService[];
  culture_guides: CultureGuide[];
  safety_info: SafetyInfo[];
  emergency_contacts: EmergencyContact[];
}

export interface ItineraryItem {
  id?: number;
  time_slot: string;
  title: string;
  category?: string;
  description: string;
  why_this?: string;
  estimated_duration_hours: number;
  estimated_cost: number;
  travel_time_from_prev?: string;
  location_name?: string;
}

export interface ItineraryDay {
  day_number: number;
  theme: string;
  overview?: string;
  estimated_day_cost: number;
  items: ItineraryItem[];
}

export interface BudgetBreakdown {
  accommodation: number;
  food: number;
  transportation: number;
  activities: number;
  shopping_misc: number;
  total: number;
  per_person: number;
  currency: string;
}

export interface Trip {
  id: number;
  title: string;
  destination_id: number;
  destination_name: string;
  country_name: string;
  travel_type: string;
  num_travellers: number;
  duration_days: number;
  start_date?: string;
  end_date?: string;
  budget_tier: string;
  budget_total: number;
  currency: string;
  pace_preference: string;
  interests: string[];
  summary?: string;
  budget_breakdown: BudgetBreakdown;
  itinerary_days: ItineraryDay[];
}

export interface User {
  id: number;
  email: string;
  full_name?: string;
}
