import React, { useEffect, useState } from 'react';
import { Bookmark, Calendar, Users, Trash2, ArrowRight, Sparkles, MapPin } from 'lucide-react';
import { api } from '../services/api';
import { Trip } from '../types';

interface SavedTripsProps {
  onSelectTrip: (tripId: number) => void;
  onStartPlanning: () => void;
}

export const SavedTripsPage: React.FC<SavedTripsProps> = ({
  onSelectTrip,
  onStartPlanning
}) => {
  const [trips, setTrips] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const fetchTrips = async () => {
    setLoading(true);
    const data = await api.getSavedTrips();
    setTrips(data);
    setLoading(false);
  };

  useEffect(() => {
    fetchTrips();
  }, []);

  const handleDelete = async (e: React.MouseEvent, id: number) => {
    e.stopPropagation();
    if (confirm('Are you sure you want to delete this trip?')) {
      await api.deleteTrip(id);
      fetchTrips();
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-10">
      <div className="flex flex-col sm:flex-row justify-between sm:items-end gap-4">
        <div>
          <span className="text-xs font-bold text-peach-dark uppercase tracking-widest block mb-1">
            Personal Itinerary Library
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight text-primary-text">
            Saved Trips
          </h1>
          <p className="text-sm text-secondary-text mt-1">
            Your planned journeys, customized schedules, and destination operating guides.
          </p>
        </div>

        <button
          onClick={onStartPlanning}
          className="flex items-center gap-2 px-6 py-3 rounded-full bg-peach hover:bg-peach-dark text-white text-xs font-semibold shadow-soft transition-all self-start sm:self-auto"
        >
          <Sparkles className="w-4 h-4" />
          <span>Plan New Trip</span>
        </button>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-pulse">
          {[1, 2, 3].map((n) => (
            <div key={n} className="h-64 rounded-3xl bg-surface-subtle border border-border" />
          ))}
        </div>
      ) : trips.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {trips.map((trip) => (
            <div
              key={trip.id}
              onClick={() => onSelectTrip(trip.id)}
              className="bg-white rounded-3xl overflow-hidden border border-border shadow-soft hover:shadow-premium transition-all duration-300 flex flex-col justify-between cursor-pointer group"
            >
              <div className="relative aspect-[16/10] overflow-hidden bg-surface-subtle">
                <img
                  src={trip.destination_thumbnail || 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=600&q=80'}
                  alt={trip.destination_name}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                />
                <span className="absolute top-4 left-4 bg-white/90 backdrop-blur-md px-3 py-1 rounded-full text-xs font-semibold text-primary-text">
                  {trip.country_name}
                </span>
                <span className="absolute top-4 right-4 bg-black/60 backdrop-blur-md px-3 py-1 rounded-full text-xs font-medium text-white">
                  {trip.travel_type}
                </span>
              </div>

              <div className="p-6 space-y-4 flex-1 flex flex-col justify-between">
                <div className="space-y-1">
                  <h3 className="text-xl font-bold text-primary-text group-hover:text-peach-dark transition-colors">
                    {trip.destination_name}
                  </h3>
                  <p className="text-xs text-secondary-text">
                    {trip.duration_days} Days • {trip.num_travellers} Travellers • {trip.budget_tier} Tier
                  </p>
                </div>

                <div className="pt-4 border-t border-border flex items-center justify-between">
                  <div>
                    <span className="text-[11px] text-secondary-text block">Est. Cost</span>
                    <span className="text-sm font-bold text-primary-text">
                      {trip.currency} {trip.budget_total?.toLocaleString()}
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      onClick={(e) => handleDelete(e, trip.id)}
                      className="p-2 text-secondary-text hover:text-red-600 transition-colors rounded-full hover:bg-surface-subtle"
                      title="Delete trip"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                    <span className="text-xs font-semibold text-peach-dark flex items-center gap-1 group-hover:translate-x-1 transition-transform">
                      Open OS →
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-24 bg-white rounded-3xl border border-border p-8 space-y-4 max-w-xl mx-auto">
          <Bookmark className="w-12 h-12 text-secondary-text mx-auto stroke-1" />
          <h3 className="text-xl font-bold text-primary-text">No saved trips yet</h3>
          <p className="text-xs text-secondary-text leading-relaxed">
            Generate your first itinerary to have your personalized day schedules, local apps, and cultural tips saved here for instant access anytime.
          </p>
          <button
            onClick={onStartPlanning}
            className="px-6 py-3 rounded-full bg-peach hover:bg-peach-dark text-white text-xs font-semibold shadow-soft transition-all"
          >
            Plan Your First Trip
          </button>
        </div>
      )}
    </div>
  );
};
