import React, { useState } from 'react';
import { 
  Users, User, Heart, Sparkles, Building2, ShieldCheck, 
  ArrowRight, ArrowLeft, Calendar, DollarSign, Check, Loader2 
} from 'lucide-react';
import { Destination, Trip } from '../types';
import { api } from '../services/api';

interface PlannerProps {
  destinations: Destination[];
  onTripGenerated: (trip: Trip) => void;
  initialDestinationId?: number | null;
}

const TRAVEL_TYPES = [
  { id: 'Solo', label: 'Solo', desc: 'Safety, budget freedom, and authentic personal discovery', icon: User },
  { id: 'Friends', label: 'Friends', desc: 'Adventure, nightlife, local food, and shared energy', icon: Users },
  { id: 'Couple', label: 'Couple', desc: 'Romantic viewpoints, intimate dinners, and cozy walks', icon: Heart },
  { id: 'Family', label: 'Family', desc: 'Child-friendly activities, safety, and relaxed comfort', icon: Users },
  { id: 'Honeymoon', label: 'Honeymoon', desc: 'Scenic luxury, private relaxation, and romantic spots', icon: Sparkles },
  { id: 'Senior Citizens', label: 'Senior Citizens', desc: 'Gentle pacing, accessibility, and restful comfort', icon: ShieldCheck },
  { id: 'Business', label: 'Business', desc: 'Efficient schedule, high connectivity, and swift transit', icon: Building2 },
  { id: 'Group Tour', label: 'Group Tour', desc: 'Organized highlights, group transport, and key sights', icon: Users },
];

const INTERESTS = [
  'Adventure', 'Nature', 'Beaches', 'History', 'Culture', 'Food',
  'Shopping', 'Nightlife', 'Photography', 'Luxury', 'Relaxation',
  'Spiritual', 'Architecture', 'Wildlife', 'Hidden Gems', 'Local Experiences'
];

const BUDGET_TIERS = [
  { id: 'Budget', label: 'Budget', desc: 'Hostels / guesthouses, public transit & local street food' },
  { id: 'Comfort', label: 'Comfort', desc: '3-star boutique hotels, mix of cabs/metro & popular cafes' },
  { id: 'Premium', label: 'Premium', desc: '4-star upscale stays, private transfers & fine dining' },
  { id: 'Luxury', label: 'Luxury', desc: '5-star resorts, VIP excursions & gourmet gastronomy' },
];

const PACING_OPTIONS = [
  { id: 'Relaxed', label: 'Relaxed Pace', desc: '1–2 activities per day, generous breaks, slow mornings' },
  { id: 'Balanced', label: 'Balanced Pace', desc: 'Optimal blend of sightseeing, meal tasting, and leisure' },
  { id: 'Packed', label: 'Packed Schedule', desc: 'Active days and nights, maximizing all major highlights' },
];

export const TripPlanner: React.FC<PlannerProps> = ({
  destinations,
  onTripGenerated,
  initialDestinationId
}) => {
  const [step, setStep] = useState<number>(1);
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [loadingStage, setLoadingStage] = useState<string>('Understanding preferences...');

  // Planner Form State
  const [travelType, setTravelType] = useState<string>('Couple');
  const [selectedDestinationId, setSelectedDestinationId] = useState<number>(initialDestinationId || (destinations[0]?.id || 1));
  const [durationDays, setDurationDays] = useState<number>(4);
  const [numTravellers, setNumTravellers] = useState<number>(2);
  const [budgetTier, setBudgetTier] = useState<string>('Comfort');
  const [selectedInterests, setSelectedInterests] = useState<string[]>(['Culture', 'Food', 'Architecture']);
  const [pacing, setPacing] = useState<string>('Balanced');
  const [notes, setNotes] = useState<string>('');

  const toggleInterest = (interest: string) => {
    if (selectedInterests.includes(interest)) {
      setSelectedInterests(selectedInterests.filter((i) => i !== interest));
    } else {
      setSelectedInterests([...selectedInterests, interest]);
    }
  };

  const handleGenerate = async () => {
    setIsGenerating(true);
    setLoadingStage('Analyzing destination profile & local seasons...');

    const stages = [
      'Personalizing day-by-day pacing for ' + travelType + ' travellers...',
      'Cross-referencing verified local transport & food apps...',
      'Auditing cultural etiquette & safety guidelines...',
      'Calculating dynamic budget distributions...',
      'Finalizing your smart trip operating dashboard...'
    ];

    let stageIdx = 0;
    const interval = setInterval(() => {
      stageIdx++;
      if (stageIdx < stages.length) {
        setLoadingStage(stages[stageIdx]);
      }
    }, 600);

    try {
      const trip = await api.generateTrip({
        destination_id: selectedDestinationId,
        travel_type: travelType,
        num_travellers: numTravellers,
        duration_days: durationDays,
        budget_tier: budgetTier,
        interests: selectedInterests,
        pace_preference: pacing,
        additional_notes: notes,
      });

      clearInterval(interval);
      if (trip) {
        onTripGenerated(trip);
      } else {
        alert('Could not generate trip. Please check your connectivity and try again.');
        setIsGenerating(false);
      }
    } catch (err) {
      clearInterval(interval);
      setIsGenerating(false);
      alert('An error occurred while generating the trip.');
    }
  };

  const totalSteps = 6;

  // Selected destination info
  const currentDest = destinations.find((d) => d.id === selectedDestinationId) || destinations[0];

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Step Progress Bar */}
      <div className="mb-10">
        <div className="flex items-center justify-between text-xs font-semibold text-secondary-text mb-3">
          <span>STEP {step} OF {totalSteps}</span>
          <span className="text-peach-dark">
            {step === 1 && "Travel Profile"}
            {step === 2 && "Destination"}
            {step === 3 && "Duration & Travellers"}
            {step === 4 && "Budget Tier"}
            {step === 5 && "Interests"}
            {step === 6 && "Pacing & Style"}
          </span>
        </div>
        <div className="h-1.5 w-full bg-surface-subtle rounded-full overflow-hidden border border-border">
          <div
            className="h-full bg-peach transition-all duration-300 rounded-full"
            style={{ width: `${(step / totalSteps) * 100}%` }}
          />
        </div>
      </div>

      {/* Main Content Area */}
      <div className="bg-white rounded-3xl p-6 sm:p-10 border border-border shadow-soft min-h-[460px] flex flex-col justify-between">
        {/* Step 1: Who's travelling? */}
        {step === 1 && (
          <div className="space-y-6">
            <div>
              <h2 className="text-2xl sm:text-3xl font-bold text-primary-text tracking-tight">Who's travelling?</h2>
              <p className="text-sm text-secondary-text mt-1">Your travel profile configures activity safety, logistics, and schedules.</p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {TRAVEL_TYPES.map((type) => {
                const IconComponent = type.icon;
                const isSelected = travelType === type.id;
                return (
                  <button
                    key={type.id}
                    onClick={() => {
                      setTravelType(type.id);
                      if (type.id === 'Solo') setNumTravellers(1);
                      if (type.id === 'Couple' || type.id === 'Honeymoon') setNumTravellers(2);
                    }}
                    className={`p-5 rounded-2xl text-left border transition-all duration-200 flex flex-col justify-between h-40 ${
                      isSelected
                        ? 'border-peach bg-peach-light/30 shadow-soft ring-1 ring-peach'
                        : 'border-border hover:border-peach/50 bg-white'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className={`w-9 h-9 rounded-xl flex items-center justify-center ${
                        isSelected ? 'bg-peach text-white' : 'bg-surface-subtle text-secondary-text'
                      }`}>
                        <IconComponent className="w-5 h-5" />
                      </div>
                      {isSelected && <Check className="w-5 h-5 text-peach-dark" />}
                    </div>
                    <div>
                      <h4 className="font-bold text-primary-text text-base">{type.label}</h4>
                      <p className="text-xs text-secondary-text mt-1 line-clamp-2">{type.desc}</p>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {/* Step 2: Where are you going? */}
        {step === 2 && (
          <div className="space-y-6">
            <div>
              <h2 className="text-2xl sm:text-3xl font-bold text-primary-text tracking-tight">Where are you going?</h2>
              <p className="text-sm text-secondary-text mt-1">Select from our verified destinations with rich local essentials.</p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {destinations.map((dest) => {
                const isSelected = selectedDestinationId === dest.id;
                return (
                  <button
                    key={dest.id}
                    onClick={() => setSelectedDestinationId(dest.id)}
                    className={`rounded-2xl border text-left overflow-hidden transition-all duration-200 group ${
                      isSelected
                        ? 'border-peach ring-2 ring-peach shadow-soft'
                        : 'border-border hover:border-peach/50'
                    }`}
                  >
                    <div className="relative h-28 w-full overflow-hidden bg-surface-subtle">
                      <img
                        src={dest.thumbnail || dest.hero_image}
                        alt={dest.name}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      />
                      <span className="absolute top-2 left-2 bg-white/90 backdrop-blur-sm px-2 py-0.5 rounded-full text-[10px] font-semibold text-primary-text">
                        {dest.country_name}
                      </span>
                    </div>
                    <div className="p-4 space-y-1 bg-white">
                      <div className="flex items-center justify-between">
                        <h4 className="font-bold text-primary-text">{dest.name}</h4>
                        {isSelected && <Check className="w-4 h-4 text-peach-dark" />}
                      </div>
                      <p className="text-xs text-secondary-text line-clamp-1">{dest.tagline}</p>
                      <p className="text-[11px] text-peach-dark font-medium pt-1">
                        From {dest.currency} {dest.approx_daily_budget} / day
                      </p>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {/* Step 3: Duration & Travellers */}
        {step === 3 && (
          <div className="space-y-8">
            <div>
              <h2 className="text-2xl sm:text-3xl font-bold text-primary-text tracking-tight">Trip duration & party size</h2>
              <p className="text-sm text-secondary-text mt-1">Configure days and travellers for accurate time planning and budget estimations.</p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-8">
              {/* Duration Days */}
              <div className="bg-surface-subtle p-6 rounded-2xl border border-border space-y-4">
                <label className="text-sm font-semibold text-primary-text block">
                  Trip Duration (Days): <span className="text-peach-dark font-bold text-lg">{durationDays} Days</span>
                </label>
                <input
                  type="range"
                  min="1"
                  max="14"
                  value={durationDays}
                  onChange={(e) => setDurationDays(parseInt(e.target.value))}
                  className="w-full accent-peach cursor-pointer"
                />
                <div className="flex justify-between text-xs text-secondary-text">
                  <span>1 Day (Weekend)</span>
                  <span>7 Days (Week)</span>
                  <span>14 Days (Extended)</span>
                </div>
              </div>

              {/* Number of Travellers */}
              <div className="bg-surface-subtle p-6 rounded-2xl border border-border space-y-4">
                <label className="text-sm font-semibold text-primary-text block">
                  Number of Travellers: <span className="text-peach-dark font-bold text-lg">{numTravellers}</span>
                </label>
                <div className="flex items-center gap-3">
                  {[1, 2, 3, 4, 5, '6+'].map((num, idx) => {
                    const val = typeof num === 'number' ? num : 6;
                    const isSelected = numTravellers === val;
                    return (
                      <button
                        key={idx}
                        onClick={() => setNumTravellers(val)}
                        className={`flex-1 py-3 rounded-xl font-bold text-sm border transition-all ${
                          isSelected
                            ? 'bg-peach text-white border-peach shadow-sm'
                            : 'bg-white border-border text-primary-text hover:bg-surface-subtle'
                        }`}
                      >
                        {num}
                      </button>
                    );
                  })}
                </div>
                <p className="text-xs text-secondary-text">
                  Accommodation costs are automatically adjusted for shared rooms.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Step 4: Budget Tier */}
        {step === 4 && (
          <div className="space-y-6">
            <div>
              <h2 className="text-2xl sm:text-3xl font-bold text-primary-text tracking-tight">What's your budget style?</h2>
              <p className="text-sm text-secondary-text mt-1">We tailor recommendations to match realistic costs in {currentDest?.name}.</p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {BUDGET_TIERS.map((tier) => {
                const isSelected = budgetTier === tier.id;
                return (
                  <button
                    key={tier.id}
                    onClick={() => setBudgetTier(tier.id)}
                    className={`p-6 rounded-2xl text-left border transition-all duration-200 flex flex-col justify-between ${
                      isSelected
                        ? 'border-peach bg-peach-light/30 shadow-soft ring-1 ring-peach'
                        : 'border-border hover:border-peach/50 bg-white'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-xs uppercase tracking-wider font-semibold text-secondary-text">Tier</span>
                      {isSelected && <Check className="w-5 h-5 text-peach-dark" />}
                    </div>
                    <div>
                      <h4 className="text-xl font-bold text-primary-text">{tier.label}</h4>
                      <p className="text-xs text-secondary-text mt-1 leading-relaxed">{tier.desc}</p>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {/* Step 5: Interests */}
        {step === 5 && (
          <div className="space-y-6">
            <div>
              <h2 className="text-2xl sm:text-3xl font-bold text-primary-text tracking-tight">What are you into?</h2>
              <p className="text-sm text-secondary-text mt-1">Select your interests to curate daily sights and activities (choose at least 2).</p>
            </div>

            <div className="flex flex-wrap gap-2.5">
              {INTERESTS.map((interest) => {
                const isSelected = selectedInterests.includes(interest);
                return (
                  <button
                    key={interest}
                    onClick={() => toggleInterest(interest)}
                    className={`px-4 py-2.5 rounded-full text-xs font-semibold border transition-all duration-150 flex items-center gap-1.5 ${
                      isSelected
                        ? 'bg-peach text-white border-peach shadow-sm'
                        : 'bg-white border-border text-secondary-text hover:text-primary-text hover:bg-surface-subtle'
                    }`}
                  >
                    {isSelected && <Check className="w-3.5 h-3.5" />}
                    <span>{interest}</span>
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {/* Step 6: Pacing & Review */}
        {step === 6 && (
          <div className="space-y-6">
            <div>
              <h2 className="text-2xl sm:text-3xl font-bold text-primary-text tracking-tight">Pacing and personal style</h2>
              <p className="text-sm text-secondary-text mt-1">How fast do you prefer moving throughout each day?</p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {PACING_OPTIONS.map((opt) => {
                const isSelected = pacing === opt.id;
                return (
                  <button
                    key={opt.id}
                    onClick={() => setPacing(opt.id)}
                    className={`p-5 rounded-2xl text-left border transition-all duration-200 ${
                      isSelected
                        ? 'border-peach bg-peach-light/30 shadow-soft ring-1 ring-peach'
                        : 'border-border hover:border-peach/50 bg-white'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-bold text-primary-text text-sm">{opt.label}</h4>
                      {isSelected && <Check className="w-4 h-4 text-peach-dark" />}
                    </div>
                    <p className="text-xs text-secondary-text leading-relaxed">{opt.desc}</p>
                  </button>
                );
              })}
            </div>

            <div>
              <label className="text-xs font-bold text-primary-text uppercase tracking-wider block mb-2">
                Additional Notes or Dietary / Mobility Preferences (Optional)
              </label>
              <textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="e.g. Vegetarian foodie, love photography at golden hour, traveling with elderly parents who need elevator access..."
                className="w-full text-sm p-4 rounded-2xl border border-border focus:outline-none focus:ring-1 focus:ring-peach bg-surface-subtle/50"
                rows={3}
              />
            </div>
          </div>
        )}

        {/* Footer Navigation Buttons */}
        <div className="pt-8 mt-8 border-t border-border flex items-center justify-between">
          {step > 1 ? (
            <button
              onClick={() => setStep(step - 1)}
              className="flex items-center gap-2 px-5 py-2.5 rounded-full border border-border text-xs font-semibold text-secondary-text hover:text-primary-text hover:bg-surface-subtle transition-all"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back</span>
            </button>
          ) : <div />}

          {step < totalSteps ? (
            <button
              onClick={() => setStep(step + 1)}
              className="flex items-center gap-2 px-6 py-3 rounded-full bg-primary-text hover:bg-black text-white text-xs font-semibold shadow-soft transition-all"
            >
              <span>Continue</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          ) : (
            <button
              onClick={handleGenerate}
              disabled={isGenerating}
              className="flex items-center gap-2 px-8 py-3.5 rounded-full bg-peach hover:bg-peach-dark text-white text-sm font-semibold shadow-soft hover:shadow-premium transition-all disabled:opacity-50"
            >
              {isGenerating ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Constructing Trip...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  <span>Generate My Trip</span>
                </>
              )}
            </button>
          )}
        </div>
      </div>

      {/* Generation Loading Overlay */}
      {isGenerating && (
        <div className="fixed inset-0 bg-primary-text/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl p-8 max-w-md w-full border border-border shadow-premium text-center space-y-6">
            <div className="w-16 h-16 rounded-2xl bg-peach-light text-peach-dark mx-auto flex items-center justify-center">
              <Loader2 className="w-8 h-8 animate-spin" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-primary-text">Creating Your Personal Travel OS</h3>
              <p className="text-xs text-secondary-text mt-1">{loadingStage}</p>
            </div>
            <div className="h-1.5 w-full bg-surface-subtle rounded-full overflow-hidden">
              <div className="h-full bg-peach animate-pulse w-3/4 rounded-full" />
            </div>
            <p className="text-[11px] text-secondary-text italic">
              Travenza connects verified local services and curated schedules without fabricating critical safety or transit info.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};
