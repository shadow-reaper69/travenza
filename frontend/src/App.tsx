import React, { useEffect, useState } from 'react';
import { Navbar } from './components/Navbar';
import { AuthModal } from './components/AuthModal';
import { LandingPage } from './pages/LandingPage';
import { TripPlanner } from './pages/TripPlanner';
import { TripDashboard } from './pages/TripDashboard';
import { ExplorePage } from './pages/ExplorePage';
import { SavedTripsPage } from './pages/SavedTripsPage';
import { api } from './services/api';
import { Destination, DestinationDetail, Trip, User } from './types';

export function App() {
  const [currentView, setCurrentView] = useState<string>('landing');
  const [destinations, setDestinations] = useState<Destination[]>([]);
  const [currentTrip, setCurrentTrip] = useState<Trip | null>(null);
  const [currentDestinationDetail, setCurrentDestinationDetail] = useState<DestinationDetail | null>(null);
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [isAuthOpen, setIsAuthOpen] = useState<boolean>(false);
  const [plannerDestinationId, setPlannerDestinationId] = useState<number | null>(null);

  // Load initial destinations and logged in user
  useEffect(() => {
    const init = async () => {
      const destList = await api.getDestinations();
      setDestinations(destList);

      const me = await api.getMe();
      if (me) setCurrentUser(me);
    };
    init();
  }, []);

  // When a destination is selected to inspect details
  const handleSelectDestination = async (destId: number) => {
    const detail = await api.getDestination(destId);
    if (detail) {
      setCurrentDestinationDetail(detail);
      // Construct a default preview trip so the full OS dashboard can be explored
      const previewTrip: Trip = {
        id: 0,
        title: `${detail.name} Travel OS`,
        destination_id: detail.id,
        destination_name: detail.name,
        country_name: detail.country_name,
        travel_type: 'Couple',
        num_travellers: 2,
        duration_days: 4,
        budget_tier: 'Comfort',
        budget_total: detail.approx_daily_budget * 4 * 2,
        currency: detail.currency,
        pace_preference: 'Balanced',
        interests: detail.interests,
        summary: detail.tagline,
        budget_breakdown: {
          accommodation: Math.round(detail.approx_daily_budget * 4 * 2 * 0.4),
          food: Math.round(detail.approx_daily_budget * 4 * 2 * 0.3),
          transportation: Math.round(detail.approx_daily_budget * 4 * 2 * 0.15),
          activities: Math.round(detail.approx_daily_budget * 4 * 2 * 0.1),
          shopping_misc: Math.round(detail.approx_daily_budget * 4 * 2 * 0.05),
          total: detail.approx_daily_budget * 4 * 2,
          per_person: detail.approx_daily_budget * 4,
          currency: detail.currency
        },
        itinerary_days: [
          {
            day_number: 1,
            theme: `Orientation & Cultural Discovery in ${detail.name}`,
            overview: `Arrival, authentic neighborhood walk, and landmark sunset viewpoints.`,
            estimated_day_cost: detail.approx_daily_budget * 2,
            items: detail.attractions.slice(0, 3).map((a, idx) => ({
              time_slot: idx === 0 ? "09:30 AM" : idx === 1 ? "01:00 PM" : "05:30 PM",
              title: a.name,
              category: a.category,
              description: a.description,
              why_this: `A highlight feature for discerning travellers in ${detail.name}.`,
              estimated_duration_hours: a.estimated_duration_hours,
              estimated_cost: a.estimated_cost,
              location_name: a.location_area || detail.name
            }))
          }
        ]
      };
      setCurrentTrip(previewTrip);
      setCurrentView('dashboard');
    }
  };

  const handleTripGenerated = async (trip: Trip) => {
    setCurrentTrip(trip);
    const detail = await api.getDestination(trip.destination_id);
    if (detail) setCurrentDestinationDetail(detail);
    setCurrentView('dashboard');
  };

  const handleOpenSavedTrip = async (tripId: number) => {
    const trip = await api.getTrip(tripId);
    if (trip) {
      setCurrentTrip(trip);
      const detail = await api.getDestination(trip.destination_id);
      if (detail) setCurrentDestinationDetail(detail);
      setCurrentView('dashboard');
    }
  };

  const handlePlanTripForDestination = (destId: number) => {
    setPlannerDestinationId(destId);
    setCurrentView('planner');
  };

  const handleLogout = () => {
    localStorage.removeItem('travenza_token');
    setCurrentUser(null);
  };

  return (
    <div className="min-h-screen bg-background flex flex-col font-sans">
      <Navbar
        currentView={currentView}
        setCurrentView={(view) => {
          if (view === 'planner') setPlannerDestinationId(null);
          setCurrentView(view);
        }}
        currentUser={currentUser}
        onOpenAuth={() => setIsAuthOpen(true)}
        onLogout={handleLogout}
      />

      <main className="flex-1">
        {currentView === 'landing' && (
          <LandingPage
            destinations={destinations}
            onStartPlanning={() => { setPlannerDestinationId(null); setCurrentView('planner'); }}
            onExplore={() => setCurrentView('explore')}
            onSelectDestination={handleSelectDestination}
          />
        )}

        {currentView === 'explore' && (
          <ExplorePage
            destinations={destinations}
            onSelectDestination={handleSelectDestination}
            onPlanTripForDestination={handlePlanTripForDestination}
          />
        )}

        {currentView === 'planner' && (
          <TripPlanner
            destinations={destinations}
            initialDestinationId={plannerDestinationId}
            onTripGenerated={handleTripGenerated}
          />
        )}

        {currentView === 'dashboard' && currentTrip && (
          <TripDashboard
            trip={currentTrip}
            destinationDetail={currentDestinationDetail}
            onPlanNew={() => { setPlannerDestinationId(null); setCurrentView('planner'); }}
          />
        )}

        {currentView === 'saved' && (
          <SavedTripsPage
            onSelectTrip={handleOpenSavedTrip}
            onStartPlanning={() => { setPlannerDestinationId(null); setCurrentView('planner'); }}
          />
        )}
      </main>

      {/* Editorial Footer */}
      <footer className="border-t border-border bg-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-peach flex items-center justify-center text-white font-bold text-sm">
              T
            </div>
            <div>
              <p className="text-sm font-bold text-primary-text">TRAVENZA</p>
              <p className="text-xs text-secondary-text">AI-Powered Smart Travel Companion & Personal Operating System</p>
            </div>
          </div>
          <div className="flex items-center gap-6 text-xs text-secondary-text">
            <span>Verified Local Intelligence</span>
            <span>•</span>
            <span>Zero Hallucinations</span>
            <span>•</span>
            <span>Safety-First Architecture</span>
          </div>
        </div>
      </footer>

      {/* Auth Modal */}
      <AuthModal
        isOpen={isAuthOpen}
        onClose={() => setIsAuthOpen(false)}
        onSuccess={(user) => setCurrentUser(user)}
      />
    </div>
  );
}

export default App;
