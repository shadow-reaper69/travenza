import React, { useState } from 'react';
import { Search, Compass, MapPin, Sparkles, Filter, ArrowRight } from 'lucide-react';
import { Destination } from '../types';

interface ExploreProps {
  destinations: Destination[];
  onSelectDestination: (id: number) => void;
  onPlanTripForDestination: (id: number) => void;
}

const CATEGORY_TABS = [
  'All',
  'Trending',
  'Beaches',
  'Culture',
  'Food',
  'Architecture',
  'Couples',
  'Solo Friendly'
];

export const ExplorePage: React.FC<ExploreProps> = ({
  destinations,
  onSelectDestination,
  onPlanTripForDestination
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');

  const filtered = destinations.filter((dest) => {
    const matchesSearch = 
      dest.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      dest.country_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      dest.tagline.toLowerCase().includes(searchQuery.toLowerCase());

    if (!matchesSearch) return false;

    if (selectedCategory === 'All') return true;
    if (selectedCategory === 'Trending') return dest.trending_score > 90;
    if (selectedCategory === 'Beaches') return dest.interests.includes('Beaches');
    if (selectedCategory === 'Culture') return dest.interests.includes('Culture') || dest.interests.includes('History');
    if (selectedCategory === 'Food') return dest.interests.includes('Food');
    if (selectedCategory === 'Architecture') return dest.interests.includes('Architecture');
    if (selectedCategory === 'Couples') return dest.travel_types.includes('Couple') || dest.travel_types.includes('Honeymoon');
    if (selectedCategory === 'Solo Friendly') return dest.travel_types.includes('Solo');

    return true;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-12">
      {/* Title & Search Bar */}
      <div className="space-y-6">
        <div>
          <span className="text-xs font-bold text-peach-dark uppercase tracking-widest block mb-1">
            Curated World Directory
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight text-primary-text">
            Explore Destinations
          </h1>
          <p className="text-sm text-secondary-text mt-2 max-w-2xl">
            Discover destinations backed by complete ground intelligence: local apps, transit systems, cultural rules, and safety helplines.
          </p>
        </div>

        {/* Search & Filter Controls */}
        <div className="flex flex-col sm:flex-row gap-4 items-center justify-between">
          <div className="relative w-full sm:max-w-md">
            <Search className="w-4 h-4 text-secondary-text absolute left-4 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search by city, country or vibe..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-11 pr-4 py-3 rounded-full border border-border bg-white text-sm focus:outline-none focus:ring-1 focus:ring-peach shadow-sm"
            />
          </div>

          {/* Category Tabs */}
          <div className="flex overflow-x-auto gap-2 w-full sm:w-auto pb-2 sm:pb-0 no-scrollbar">
            {CATEGORY_TABS.map((tab) => (
              <button
                key={tab}
                onClick={() => setSelectedCategory(tab)}
                className={`px-4 py-2 rounded-full text-xs font-semibold whitespace-nowrap transition-all ${
                  selectedCategory === tab
                    ? 'bg-peach text-white shadow-soft'
                    : 'bg-white border border-border text-secondary-text hover:text-primary-text hover:bg-surface-subtle'
                }`}
              >
                {tab}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Destinations Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
        {filtered.map((dest) => (
          <div
            key={dest.id}
            className="bg-white rounded-3xl overflow-hidden border border-border shadow-soft hover:shadow-premium transition-all duration-300 flex flex-col justify-between group"
          >
            <div className="relative aspect-[16/11] overflow-hidden bg-surface-subtle">
              <img
                src={dest.hero_image}
                alt={dest.name}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              />
              <span className="absolute top-4 left-4 bg-white/90 backdrop-blur-md px-3 py-1 rounded-full text-xs font-semibold text-primary-text">
                {dest.country_name}
              </span>
              <span className="absolute top-4 right-4 bg-black/60 backdrop-blur-md px-3 py-1 rounded-full text-xs font-medium text-white">
                Score {dest.trending_score}
              </span>
            </div>

            <div className="p-6 space-y-4 flex-1 flex flex-col justify-between">
              <div className="space-y-2">
                <h3 className="text-2xl font-bold text-primary-text group-hover:text-peach-dark transition-colors">
                  {dest.name}
                </h3>
                <p className="text-xs text-secondary-text line-clamp-2 leading-relaxed">
                  {dest.tagline}
                </p>

                <div className="flex flex-wrap gap-1.5 pt-2">
                  {dest.interests.map((intName, idx) => (
                    <span
                      key={idx}
                      className="text-[10px] font-medium bg-surface-subtle text-secondary-text px-2 py-0.5 rounded-full"
                    >
                      {intName}
                    </span>
                  ))}
                </div>
              </div>

              <div className="pt-4 border-t border-border space-y-3">
                <div className="flex items-center justify-between text-xs text-secondary-text">
                  <span>Est. Daily Budget</span>
                  <span className="font-bold text-primary-text">{dest.currency} {dest.approx_daily_budget}</span>
                </div>

                <div className="grid grid-cols-2 gap-2">
                  <button
                    onClick={() => onSelectDestination(dest.id)}
                    className="py-2.5 rounded-xl border border-border text-xs font-semibold text-primary-text hover:bg-surface-subtle transition-all text-center"
                  >
                    View Guide
                  </button>
                  <button
                    onClick={() => onPlanTripForDestination(dest.id)}
                    className="py-2.5 rounded-xl bg-peach hover:bg-peach-dark text-white text-xs font-semibold shadow-soft transition-all text-center flex items-center justify-center gap-1"
                  >
                    <Sparkles className="w-3.5 h-3.5" />
                    <span>Plan Trip</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filtered.length === 0 && (
        <div className="text-center py-20 bg-white rounded-3xl border border-border p-8 space-y-4">
          <Compass className="w-12 h-12 text-secondary-text mx-auto stroke-1" />
          <h3 className="text-xl font-bold text-primary-text">No destinations matched</h3>
          <p className="text-xs text-secondary-text max-w-sm mx-auto">
            Try adjusting your search query or reset your category filters to browse all verified destinations.
          </p>
          <button
            onClick={() => { setSearchQuery(''); setSelectedCategory('All'); }}
            className="px-5 py-2.5 rounded-full bg-surface-subtle text-xs font-semibold text-primary-text hover:bg-border transition-all"
          >
            Clear Filters
          </button>
        </div>
      )}
    </div>
  );
};
