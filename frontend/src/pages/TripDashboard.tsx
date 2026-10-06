import React, { useState } from 'react';
import { 
  Calendar, Users, DollarSign, Clock, MapPin, Sparkles, 
  Smartphone, BookOpen, ShieldAlert, Share2, BookmarkCheck,
  ChevronRight, AlertCircle, Compass, CheckCircle2, PhoneCall
} from 'lucide-react';
import { Trip, DestinationDetail } from '../types';

interface DashboardProps {
  trip: Trip;
  destinationDetail: DestinationDetail | null;
  onPlanNew: () => void;
}

export const TripDashboard: React.FC<DashboardProps> = ({
  trip,
  destinationDetail,
  onPlanNew
}) => {
  const [activeTab, setActiveTab] = useState<string>('itinerary');
  const [selectedDayNumber, setSelectedDayNumber] = useState<number>(1);
  const [copiedLink, setCopiedLink] = useState<boolean>(false);

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'itinerary', label: 'Day-Wise Itinerary' },
    { id: 'budget', label: 'Budget Breakdown' },
    { id: 'essentials', label: 'Local Essentials' },
    { id: 'culture', label: 'Culture & Etiquette' },
    { id: 'safety', label: 'Safety & Emergency' },
  ];

  const handleShare = () => {
    navigator.clipboard.writeText(window.location.href);
    setCopiedLink(true);
    setTimeout(() => setCopiedLink(false), 2000);
  };

  const currentDay = trip.itinerary_days.find((d) => d.day_number === selectedDayNumber) || trip.itinerary_days[0];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Editorial Header Banner */}
      <div className="bg-white rounded-3xl p-6 sm:p-10 border border-border shadow-soft relative overflow-hidden">
        <div className="flex flex-col lg:flex-row justify-between lg:items-center gap-6">
          <div className="space-y-3">
            <div className="flex flex-wrap items-center gap-2">
              <span className="px-3 py-1 rounded-full bg-peach-light text-peach-dark font-semibold text-xs uppercase tracking-wide">
                {trip.travel_type} Travel
              </span>
              <span className="px-3 py-1 rounded-full bg-surface-subtle text-secondary-text font-medium text-xs">
                {trip.duration_days} Days / {trip.num_travellers} {trip.num_travellers === 1 ? 'Traveller' : 'Travellers'}
              </span>
              <span className="px-3 py-1 rounded-full bg-surface-subtle text-secondary-text font-medium text-xs">
                {trip.budget_tier} Tier
              </span>
            </div>

            <h1 className="text-3xl sm:text-5xl font-bold tracking-tight text-primary-text">
              {trip.destination_name}
              <span className="text-secondary-text font-light text-2xl sm:text-4xl ml-3">
                {trip.country_name}
              </span>
            </h1>

            <p className="text-sm text-secondary-text max-w-3xl leading-relaxed">
              {trip.summary || `Personalized trip curated for ${trip.travel_type} travellers focusing on ${trip.interests.join(', ')}.`}
            </p>
          </div>

          {/* Action CTAs */}
          <div className="flex items-center gap-3 self-start lg:self-center">
            <button
              onClick={handleShare}
              className="flex items-center gap-2 px-4 py-2.5 rounded-full border border-border bg-white hover:bg-surface-subtle text-xs font-semibold text-primary-text transition-all shadow-sm"
            >
              <Share2 className="w-4 h-4" />
              <span>{copiedLink ? 'Copied Link!' : 'Share Trip'}</span>
            </button>
            <button
              onClick={onPlanNew}
              className="flex items-center gap-2 px-5 py-2.5 rounded-full bg-peach hover:bg-peach-dark text-white text-xs font-semibold shadow-soft transition-all"
            >
              <Sparkles className="w-4 h-4" />
              <span>Plan Another Trip</span>
            </button>
          </div>
        </div>

        {/* Tab Navigation Pill Bar */}
        <div className="flex overflow-x-auto gap-2 pt-8 mt-8 border-t border-border no-scrollbar">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-5 py-2.5 rounded-full text-xs font-semibold whitespace-nowrap transition-all duration-200 ${
                activeTab === tab.id
                  ? 'bg-primary-text text-white shadow-soft'
                  : 'bg-surface-subtle text-secondary-text hover:text-primary-text hover:bg-surface-subtle/80'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* TAB 1: OVERVIEW */}
      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <div className="lg:col-span-8 space-y-8">
            {/* Quick Sights Card */}
            <div className="bg-white p-8 rounded-3xl border border-border shadow-soft space-y-6">
              <h3 className="text-xl font-bold text-primary-text">Destination Highlights</h3>
              <p className="text-sm text-secondary-text leading-relaxed">
                {destinationDetail?.description || 'Explore the rich heritage and contemporary lifestyle of this premier destination.'}
              </p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
                {destinationDetail?.attractions.slice(0, 4).map((attr) => (
                  <div key={attr.id} className="p-4 rounded-2xl bg-surface-subtle border border-border/60 space-y-1">
                    <span className="text-[10px] font-bold text-peach-dark uppercase tracking-wider">{attr.category}</span>
                    <h4 className="font-bold text-primary-text text-sm">{attr.name}</h4>
                    <p className="text-xs text-secondary-text line-clamp-2">{attr.description}</p>
                    <p className="text-[11px] text-secondary-text font-medium pt-1">
                      Est. Duration: {attr.estimated_duration_hours}h • Area: {attr.location_area || 'Central'}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Travel operating tips */}
            <div className="bg-peach-light/20 p-8 rounded-3xl border border-peach/20 space-y-4">
              <div className="flex items-center gap-2 text-peach-dark">
                <Sparkles className="w-5 h-5" />
                <h3 className="text-base font-bold">Travenza Operating Advice</h3>
              </div>
              <ul className="text-xs text-primary-text/80 space-y-2 leading-relaxed">
                <li>• Best season to visit: <strong>{destinationDetail?.best_time_to_visit || 'Year-round'}</strong>.</li>
                <li>• Pacing: Tailored for <strong>{trip.pace_preference}</strong> days with built-in transit allowances between zones.</li>
                <li>• Cash vs. Digital: Check the Local Essentials tab for specific contactless apps and SIM details before departure.</li>
              </ul>
            </div>
          </div>

          {/* Right Column: Quick Stats */}
          <div className="lg:col-span-4 space-y-6">
            <div className="bg-white p-6 rounded-3xl border border-border shadow-soft space-y-4">
              <h3 className="text-base font-bold text-primary-text">Trip Snapshot</h3>
              
              <div className="space-y-3 divide-y divide-border text-xs">
                <div className="flex justify-between py-2">
                  <span className="text-secondary-text">Total Days</span>
                  <span className="font-bold text-primary-text">{trip.duration_days} Days</span>
                </div>
                <div className="flex justify-between py-2">
                  <span className="text-secondary-text">Travel Persona</span>
                  <span className="font-bold text-primary-text">{trip.travel_type}</span>
                </div>
                <div className="flex justify-between py-2">
                  <span className="text-secondary-text">Budget Tier</span>
                  <span className="font-bold text-primary-text">{trip.budget_tier}</span>
                </div>
                <div className="flex justify-between py-2">
                  <span className="text-secondary-text">Est. Total Expense</span>
                  <span className="font-bold text-peach-dark text-sm">
                    {trip.currency} {trip.budget_breakdown?.total.toLocaleString()}
                  </span>
                </div>
                <div className="flex justify-between py-2">
                  <span className="text-secondary-text">Per Person Estimate</span>
                  <span className="font-bold text-primary-text">
                    {trip.currency} {trip.budget_breakdown?.per_person.toLocaleString()}
                  </span>
                </div>
              </div>
            </div>

            {/* Quick Emergency Widget */}
            <div className="bg-white p-6 rounded-3xl border border-border shadow-soft space-y-3">
              <div className="flex items-center gap-2 text-red-600">
                <PhoneCall className="w-4 h-4" />
                <h4 className="text-sm font-bold text-primary-text">Emergency Dispatch</h4>
              </div>
              <div className="space-y-2">
                {destinationDetail?.emergency_contacts.slice(0, 2).map((ec) => (
                  <div key={ec.id} className="flex justify-between items-center text-xs py-1.5 border-b border-border/50">
                    <span className="text-secondary-text">{ec.service_type}</span>
                    <span className="font-mono font-bold text-red-600">{ec.contact_number}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: DAY-WISE ITINERARY */}
      {activeTab === 'itinerary' && (
        <div className="space-y-8">
          {/* Day Selector Pills */}
          <div className="flex overflow-x-auto gap-2 pb-2 no-scrollbar">
            {trip.itinerary_days.map((day) => (
              <button
                key={day.day_number}
                onClick={() => setSelectedDayNumber(day.day_number)}
                className={`px-5 py-3 rounded-2xl text-xs font-semibold whitespace-nowrap transition-all duration-200 border ${
                  selectedDayNumber === day.day_number
                    ? 'bg-peach text-white border-peach shadow-soft'
                    : 'bg-white border-border text-secondary-text hover:text-primary-text hover:bg-surface-subtle'
                }`}
              >
                Day {day.day_number}: {day.theme.split('&')[0]}
              </button>
            ))}
          </div>

          {/* Current Day Schedule */}
          {currentDay && (
            <div className="bg-white rounded-3xl p-6 sm:p-10 border border-border shadow-soft space-y-8">
              <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-4 pb-6 border-b border-border">
                <div>
                  <span className="text-xs font-bold text-peach-dark uppercase tracking-widest">
                    DAY {currentDay.day_number}
                  </span>
                  <h3 className="text-2xl font-bold text-primary-text mt-1">{currentDay.theme}</h3>
                  <p className="text-xs text-secondary-text mt-1">{currentDay.overview}</p>
                </div>
                <div className="text-right sm:text-right">
                  <span className="text-[11px] text-secondary-text block">Est. Day Cost</span>
                  <span className="text-lg font-bold text-primary-text">
                    {trip.currency} {currentDay.estimated_day_cost.toLocaleString()}
                  </span>
                </div>
              </div>

              {/* Day Items Timeline */}
              <div className="space-y-6 relative before:absolute before:inset-0 before:left-5 before:w-0.5 before:bg-border">
                {currentDay.items.map((item, idx) => (
                  <div key={idx} className="relative flex items-start gap-6 group">
                    {/* Time Pill Dot */}
                    <div className="w-10 h-10 rounded-full bg-peach-light text-peach-dark border-4 border-white shadow-sm flex items-center justify-center font-bold text-xs shrink-0 z-10">
                      {idx + 1}
                    </div>

                    {/* Schedule Content Card */}
                    <div className="flex-1 bg-surface-subtle/60 hover:bg-surface-subtle rounded-2xl p-6 border border-border/80 transition-all space-y-3">
                      <div className="flex flex-wrap items-center justify-between gap-2">
                        <div className="flex items-center gap-2">
                          <span className="px-2.5 py-1 rounded-md bg-white text-xs font-mono font-bold text-primary-text border border-border">
                            {item.time_slot}
                          </span>
                          <span className="text-xs font-semibold text-peach-dark uppercase tracking-wide">
                            {item.category}
                          </span>
                        </div>
                        <span className="text-xs text-secondary-text font-medium">
                          Est. Cost: <strong className="text-primary-text">{trip.currency} {item.estimated_cost}</strong>
                        </span>
                      </div>

                      <h4 className="text-lg font-bold text-primary-text">{item.title}</h4>
                      <p className="text-sm text-secondary-text leading-relaxed">{item.description}</p>

                      {item.why_this && (
                        <div className="p-3 rounded-xl bg-white/70 border border-border/50 text-xs text-secondary-text">
                          <strong className="text-primary-text">Why this? </strong>
                          {item.why_this}
                        </div>
                      )}

                      <div className="flex flex-wrap gap-4 pt-2 text-xs text-secondary-text border-t border-border/40">
                        {item.location_name && (
                          <span className="flex items-center gap-1">
                            <MapPin className="w-3.5 h-3.5 text-secondary-text" />
                            {item.location_name}
                          </span>
                        )}
                        <span className="flex items-center gap-1">
                          <Clock className="w-3.5 h-3.5 text-secondary-text" />
                          Duration: {item.estimated_duration_hours}h
                        </span>
                        {item.travel_time_from_prev && (
                          <span className="flex items-center gap-1 text-peach-dark font-medium">
                            • Transit: {item.travel_time_from_prev}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* TAB 3: BUDGET BREAKDOWN */}
      {activeTab === 'budget' && (
        <div className="bg-white rounded-3xl p-6 sm:p-10 border border-border shadow-soft space-y-8">
          <div>
            <span className="text-xs font-bold text-peach-dark uppercase tracking-widest">Financial Transparency</span>
            <h2 className="text-2xl sm:text-3xl font-bold text-primary-text mt-1">Estimated Budget Breakdown</h2>
            <p className="text-xs text-secondary-text mt-1">
              All numbers are estimated projections calculated from real destination price baselines.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-6 rounded-2xl bg-surface-subtle border border-border space-y-2">
              <span className="text-xs text-secondary-text font-medium">Total Trip Estimate</span>
              <p className="text-3xl font-bold text-primary-text">
                {trip.currency} {trip.budget_breakdown?.total.toLocaleString()}
              </p>
              <p className="text-xs text-secondary-text">For all {trip.num_travellers} travellers over {trip.duration_days} days</p>
            </div>

            <div className="p-6 rounded-2xl bg-surface-subtle border border-border space-y-2">
              <span className="text-xs text-secondary-text font-medium">Per Person Projection</span>
              <p className="text-3xl font-bold text-peach-dark">
                {trip.currency} {trip.budget_breakdown?.per_person.toLocaleString()}
              </p>
              <p className="text-xs text-secondary-text">Inclusive of accommodation, dining & activities</p>
            </div>

            <div className="p-6 rounded-2xl bg-surface-subtle border border-border space-y-2">
              <span className="text-xs text-secondary-text font-medium">Daily Velocity</span>
              <p className="text-3xl font-bold text-primary-text">
                {trip.currency} {Math.round((trip.budget_breakdown?.total || 0) / trip.duration_days).toLocaleString()}
              </p>
              <p className="text-xs text-secondary-text">Average combined daily spending</p>
            </div>
          </div>

          {/* Allocation Categories */}
          <div className="space-y-4 pt-4">
            <h3 className="text-lg font-bold text-primary-text">Category Distributions</h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
              <div className="p-5 rounded-2xl border border-border bg-white space-y-1">
                <span className="text-xs text-secondary-text font-semibold uppercase">Accommodation</span>
                <p className="text-xl font-bold text-primary-text">
                  {trip.currency} {trip.budget_breakdown?.accommodation.toLocaleString()}
                </p>
                <p className="text-[11px] text-secondary-text">Hotels / Stays</p>
              </div>

              <div className="p-5 rounded-2xl border border-border bg-white space-y-1">
                <span className="text-xs text-secondary-text font-semibold uppercase">Food & Dining</span>
                <p className="text-xl font-bold text-primary-text">
                  {trip.currency} {trip.budget_breakdown?.food.toLocaleString()}
                </p>
                <p className="text-[11px] text-secondary-text">Local meals & cafes</p>
              </div>

              <div className="p-5 rounded-2xl border border-border bg-white space-y-1">
                <span className="text-xs text-secondary-text font-semibold uppercase">Transportation</span>
                <p className="text-xl font-bold text-primary-text">
                  {trip.currency} {trip.budget_breakdown?.transportation.toLocaleString()}
                </p>
                <p className="text-[11px] text-secondary-text">Metro, cabs & transit</p>
              </div>

              <div className="p-5 rounded-2xl border border-border bg-white space-y-1">
                <span className="text-xs text-secondary-text font-semibold uppercase">Activities & Entry</span>
                <p className="text-xl font-bold text-primary-text">
                  {trip.currency} {trip.budget_breakdown?.activities.toLocaleString()}
                </p>
                <p className="text-[11px] text-secondary-text">Monument tickets & tours</p>
              </div>

              <div className="p-5 rounded-2xl border border-border bg-white space-y-1">
                <span className="text-xs text-secondary-text font-semibold uppercase">Shopping / Misc</span>
                <p className="text-xl font-bold text-primary-text">
                  {trip.currency} {trip.budget_breakdown?.shopping_misc.toLocaleString()}
                </p>
                <p className="text-[11px] text-secondary-text">Souvenirs & reserve</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 4: LOCAL ESSENTIALS GUIDE */}
      {activeTab === 'essentials' && (
        <div className="bg-white rounded-3xl p-6 sm:p-10 border border-border shadow-soft space-y-8">
          <div>
            <span className="text-xs font-bold text-peach-dark uppercase tracking-widest">Ground Intelligence</span>
            <h2 className="text-2xl sm:text-3xl font-bold text-primary-text mt-1">Local Essentials & Apps</h2>
            <p className="text-xs text-secondary-text mt-1">
              The essential digital tools and transport services actually used by locals and travellers in {trip.destination_name}.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {destinationDetail?.local_services.map((svc) => (
              <div key={svc.id} className="p-6 rounded-2xl bg-surface-subtle border border-border flex flex-col justify-between space-y-4">
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-bold text-peach-dark uppercase tracking-wider">
                      {svc.category}
                    </span>
                    <span className="text-[11px] text-secondary-text bg-white px-2 py-0.5 rounded-full border border-border">
                      {svc.platform}
                    </span>
                  </div>
                  <h4 className="text-lg font-bold text-primary-text">{svc.name}</h4>
                  <p className="text-xs font-medium text-secondary-text">{svc.purpose}</p>
                  <p className="text-xs text-secondary-text leading-relaxed pt-2">{svc.explanation}</p>
                </div>

                {svc.app_link && (
                  <a
                    href={svc.app_link}
                    target="_blank"
                    rel="noreferrer"
                    className="text-xs font-semibold text-peach-dark hover:underline inline-flex items-center gap-1 pt-2"
                  >
                    Official Link / App →
                  </a>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 5: CULTURE GUIDE (KNOW BEFORE YOU GO) */}
      {activeTab === 'culture' && (
        <div className="bg-white rounded-3xl p-6 sm:p-10 border border-border shadow-soft space-y-8">
          <div>
            <span className="text-xs font-bold text-peach-dark uppercase tracking-widest">Cultural Intelligence</span>
            <h2 className="text-2xl sm:text-3xl font-bold text-primary-text mt-1">Know Before You Go</h2>
            <p className="text-xs text-secondary-text mt-1">
              Nuanced cultural respect, etiquette norms, dining traditions, and helpful everyday phrases.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {destinationDetail?.culture_guides.map((cg) => {
              const isDo = cg.category === 'DO';
              const isDont = cg.category === 'DONT';
              return (
                <div
                  key={cg.id}
                  className={`p-6 rounded-2xl border transition-all space-y-3 ${
                    isDo
                      ? 'bg-emerald-50/40 border-emerald-200'
                      : isDont
                      ? 'bg-rose-50/40 border-rose-200'
                      : 'bg-surface-subtle border-border'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className={`text-[11px] font-bold uppercase tracking-wider ${
                      isDo ? 'text-emerald-700' : isDont ? 'text-rose-700' : 'text-peach-dark'
                    }`}>
                      {cg.category}
                    </span>
                    <span className="text-[10px] text-secondary-text font-medium bg-white px-2 py-0.5 rounded-full border border-border">
                      {cg.importance_level}
                    </span>
                  </div>

                  <h4 className="text-base font-bold text-primary-text">{cg.title}</h4>
                  <p className="text-xs text-secondary-text leading-relaxed">{cg.description}</p>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* TAB 6: SAFETY & EMERGENCY CENTER */}
      {activeTab === 'safety' && (
        <div className="space-y-8">
          {/* Emergency Helplines Banner */}
          <div className="bg-rose-50 border border-rose-200 rounded-3xl p-6 sm:p-8 space-y-4">
            <div className="flex items-center gap-2 text-rose-700">
              <ShieldAlert className="w-6 h-6" />
              <h3 className="text-lg font-bold">Verified Emergency Contacts</h3>
            </div>
            <p className="text-xs text-rose-900/80">
              Save these contacts to your phone contacts before arriving. Travenza validates dispatch helplines directly with official state tourism and emergency services.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 pt-2">
              {destinationDetail?.emergency_contacts.map((ec) => (
                <div key={ec.id} className="bg-white p-4 rounded-xl border border-rose-200/80 shadow-sm space-y-1">
                  <span className="text-[11px] text-secondary-text block">{ec.service_type}</span>
                  <p className="text-2xl font-mono font-bold text-rose-700">{ec.contact_number}</p>
                  {ec.notes && <p className="text-[10px] text-secondary-text">{ec.notes}</p>}
                </div>
              ))}
            </div>
          </div>

          {/* Safety Warnings & Scams */}
          <div className="bg-white rounded-3xl p-6 sm:p-10 border border-border shadow-soft space-y-6">
            <h3 className="text-xl font-bold text-primary-text">Safety Advisories & Scam Awareness</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {destinationDetail?.safety_info.map((si) => (
                <div key={si.id} className="p-6 rounded-2xl bg-surface-subtle border border-border space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-bold text-peach-dark uppercase tracking-wider">
                      {si.category}
                    </span>
                    <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${
                      si.severity === 'Warning' ? 'bg-red-100 text-red-700' : 'bg-amber-100 text-amber-800'
                    }`}>
                      {si.severity}
                    </span>
                  </div>
                  <h4 className="text-base font-bold text-primary-text">{si.title}</h4>
                  <p className="text-xs text-secondary-text leading-relaxed">{si.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
