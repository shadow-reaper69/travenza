import React from 'react';
import { ArrowRight, Compass, ShieldCheck, Smartphone, BookOpen, Clock, HeartHandshake, Sparkles, CheckCircle2 } from 'lucide-react';
import { Destination } from '../types';

interface LandingProps {
  destinations: Destination[];
  onStartPlanning: () => void;
  onExplore: () => void;
  onSelectDestination: (id: number) => void;
}

export const LandingPage: React.FC<LandingProps> = ({
  destinations,
  onStartPlanning,
  onExplore,
  onSelectDestination
}) => {
  return (
    <div className="space-y-24 pb-24">
      {/* Editorial Hero Section */}
      <section className="relative pt-12 md:pt-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          
          <div className="lg:col-span-7 space-y-8">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-peach-light/70 text-peach-dark text-xs font-semibold tracking-wide uppercase">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Personal Travel Operating System</span>
            </div>

            <h1 className="text-4xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-primary-text leading-[1.08]">
              Travel smarter.<br />
              <span className="text-secondary-text font-normal">Experience more.</span>
            </h1>

            <p className="text-lg sm:text-xl text-secondary-text leading-relaxed max-w-2xl font-light">
              Plan your complete trip, discover verified local essentials, understand cultural etiquette, and explore with quiet confidence — all from one single platform.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 pt-2">
              <button
                onClick={onStartPlanning}
                className="flex items-center justify-center gap-3 px-8 py-4 rounded-full bg-peach hover:bg-peach-dark text-white font-medium text-base shadow-soft hover:shadow-premium transition-all duration-200 group"
              >
                <span>Plan My Trip</span>
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </button>

              <button
                onClick={onExplore}
                className="flex items-center justify-center gap-2 px-8 py-4 rounded-full bg-surface hover:bg-surface-subtle text-primary-text font-medium text-base border border-border transition-all duration-200"
              >
                <Compass className="w-4 h-4 text-secondary-text" />
                <span>Explore Destinations</span>
              </button>
            </div>

            {/* Micro stats banner */}
            <div className="grid grid-cols-3 gap-6 pt-6 border-t border-border">
              <div>
                <p className="text-2xl sm:text-3xl font-bold text-primary-text">8+</p>
                <p className="text-xs text-secondary-text font-medium uppercase tracking-wider mt-1">Travel Profiles</p>
              </div>
              <div>
                <p className="text-2xl sm:text-3xl font-bold text-primary-text">100%</p>
                <p className="text-xs text-secondary-text font-medium uppercase tracking-wider mt-1">Verified Essentials</p>
              </div>
              <div>
                <p className="text-2xl sm:text-3xl font-bold text-primary-text">Zero</p>
                <p className="text-xs text-secondary-text font-medium uppercase tracking-wider mt-1">Hallucinations</p>
              </div>
            </div>
          </div>

          {/* Hero Visual Card Composition */}
          <div className="lg:col-span-5 relative">
            <div className="relative mx-auto max-w-md lg:max-w-none">
              <div className="relative rounded-3xl overflow-hidden shadow-premium border border-border aspect-[4/5] bg-surface-subtle group">
                <img
                  src="https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=1200&q=80"
                  alt="Tokyo cityscape and temple"
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-primary-text/90 via-primary-text/20 to-transparent"></div>

                <div className="absolute bottom-6 left-6 right-6 text-white space-y-2">
                  <span className="text-xs uppercase tracking-widest bg-white/20 backdrop-blur-md px-3 py-1 rounded-full text-white inline-block">
                    Trending This Month
                  </span>
                  <h3 className="text-2xl font-bold">Tokyo, Japan</h3>
                  <p className="text-sm text-white/80 line-clamp-2">
                    Futuristic neon metropolises seamlessly interwoven with timeless Shinto tranquility.
                  </p>
                  <div className="pt-2 flex items-center justify-between text-xs text-white/90 border-t border-white/20">
                    <span>From ¥14,000 / day</span>
                    <span className="underline cursor-pointer" onClick={() => onSelectDestination(2)}>
                      View Guide →
                    </span>
                  </div>
                </div>
              </div>

              {/* Floating Smart Widget Overlay */}
              <div className="absolute -bottom-6 -left-6 bg-white p-4 rounded-2xl shadow-premium border border-border max-w-[240px] hidden sm:block animate-pulse duration-1000">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-peach-light text-peach-dark flex items-center justify-center font-bold">
                    <Smartphone className="w-5 h-5" />
                  </div>
                  <div>
                    <p className="text-xs font-bold text-primary-text">Transit: Suica Card</p>
                    <p className="text-[11px] text-secondary-text">Digital wallet ready</p>
                  </div>
                </div>
              </div>

              {/* Floating Cultural Note Widget */}
              <div className="absolute -top-6 -right-6 bg-white p-4 rounded-2xl shadow-premium border border-border max-w-[240px] hidden sm:block">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-green-50 text-emerald-600 flex items-center justify-center font-bold">
                    <CheckCircle2 className="w-5 h-5" />
                  </div>
                  <div>
                    <p className="text-xs font-bold text-primary-text">Tipping Etiquette</p>
                    <p className="text-[11px] text-secondary-text">Zero tipping expected</p>
                  </div>
                </div>
              </div>

            </div>
          </div>

        </div>
      </section>

      {/* Philosophy: Beyond Generic Booking Sites */}
      <section className="bg-surface-subtle py-20 border-y border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto space-y-4">
            <h2 className="text-xs uppercase tracking-widest font-bold text-peach-dark">Why Travenza Exists</h2>
            <p className="text-3xl sm:text-4xl font-bold text-primary-text tracking-tight">
              One platform that answers what to do, what it costs, and how to behave.
            </p>
            <p className="text-base text-secondary-text leading-relaxed font-light">
              Don’t juggle 12 tabs between travel blogs, transit forums, currency calculators, and emergency phone directories. Travenza organizes verified local intelligence into a single calm interface.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mt-16">
            <div className="bg-white p-8 rounded-2xl border border-border shadow-soft space-y-4">
              <div className="w-12 h-12 rounded-xl bg-peach-light text-peach-dark flex items-center justify-center">
                <Compass className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-primary-text">Personalized Pacing</h3>
              <p className="text-sm text-secondary-text leading-relaxed">
                Itineraries tailored for Solo explorers, Couples, Honeymoons, or Friends groups with realistic transit times.
              </p>
            </div>

            <div className="bg-white p-8 rounded-2xl border border-border shadow-soft space-y-4">
              <div className="w-12 h-12 rounded-xl bg-peach-light text-peach-dark flex items-center justify-center">
                <Smartphone className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-primary-text">Local Apps & Mobility</h3>
              <p className="text-sm text-secondary-text leading-relaxed">
                Know which ride-hailing apps, payment QR systems, and eSIMs work in each destination before boarding.
              </p>
            </div>

            <div className="bg-white p-8 rounded-2xl border border-border shadow-soft space-y-4">
              <div className="w-12 h-12 rounded-xl bg-peach-light text-peach-dark flex items-center justify-center">
                <BookOpen className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-primary-text">Cultural Etiquette</h3>
              <p className="text-sm text-secondary-text leading-relaxed">
                Nuanced Do’s and Don’ts, sacred temple dress codes, tipping etiquette, and polite everyday phrases.
              </p>
            </div>

            <div className="bg-white p-8 rounded-2xl border border-border shadow-soft space-y-4">
              <div className="w-12 h-12 rounded-xl bg-peach-light text-peach-dark flex items-center justify-center">
                <ShieldCheck className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-primary-text">Verified Safety Center</h3>
              <p className="text-sm text-secondary-text leading-relaxed">
                Verified national emergency numbers, tourist assistance helplines, and region-specific scam awareness.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Destinations Carousel */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-10 gap-4">
          <div>
            <span className="text-xs font-bold uppercase tracking-widest text-peach-dark block mb-2">Curated Highlights</span>
            <h2 className="text-3xl font-bold text-primary-text tracking-tight">Popular Destinations</h2>
          </div>
          <button
            onClick={onExplore}
            className="text-sm font-semibold text-primary-text hover:text-peach-dark flex items-center gap-1 transition-colors"
          >
            <span>View all destinations</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {destinations.slice(0, 6).map((dest) => (
            <div
              key={dest.id}
              onClick={() => onSelectDestination(dest.id)}
              className="bg-white rounded-2xl overflow-hidden border border-border shadow-soft hover:shadow-premium transition-all duration-300 cursor-pointer group flex flex-col"
            >
              <div className="relative aspect-[16/10] overflow-hidden bg-surface-subtle">
                <img
                  src={dest.hero_image}
                  alt={dest.name}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                />
                <span className="absolute top-4 left-4 bg-white/90 backdrop-blur-md px-3 py-1 rounded-full text-xs font-semibold text-primary-text">
                  {dest.country_name}
                </span>
                <span className="absolute top-4 right-4 bg-black/50 backdrop-blur-md px-3 py-1 rounded-full text-xs font-medium text-white">
                  Score {dest.trending_score}
                </span>
              </div>

              <div className="p-6 flex-1 flex flex-col justify-between space-y-4">
                <div>
                  <h3 className="text-xl font-bold text-primary-text group-hover:text-peach-dark transition-colors">
                    {dest.name}
                  </h3>
                  <p className="text-sm text-secondary-text mt-1 line-clamp-2">
                    {dest.tagline}
                  </p>
                </div>

                <div className="flex flex-wrap gap-1.5">
                  {dest.interests.slice(0, 3).map((intName, idx) => (
                    <span
                      key={idx}
                      className="text-[11px] font-medium bg-surface-subtle text-secondary-text px-2.5 py-1 rounded-full"
                    >
                      {intName}
                    </span>
                  ))}
                </div>

                <div className="pt-4 border-t border-border flex items-center justify-between text-xs text-secondary-text">
                  <span>Est. Daily: <strong className="text-primary-text">{dest.currency} {dest.approx_daily_budget}</strong></span>
                  <span className="font-semibold text-peach-dark flex items-center gap-1">
                    Explore Details →
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Start Planning CTA Bar */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-primary-text text-white rounded-3xl p-8 sm:p-14 relative overflow-hidden flex flex-col lg:flex-row items-center justify-between gap-8">
          <div className="space-y-4 max-w-2xl">
            <span className="text-xs uppercase tracking-widest text-peach font-bold">Ready to take off?</span>
            <h2 className="text-3xl sm:text-4xl font-bold tracking-tight">
              Build your customized itinerary in under 60 seconds.
            </h2>
            <p className="text-sm sm:text-base text-white/70">
              Pick your travelling profile, destination, dates, budget tier, and preferred interests. Travenza constructs an intelligent daily schedule and verified essentials guide.
            </p>
          </div>
          <button
            onClick={onStartPlanning}
            className="whitespace-nowrap px-8 py-4 rounded-full bg-peach hover:bg-peach-dark text-white font-medium text-base shadow-soft hover:shadow-premium transition-all duration-200"
          >
            Start Trip Planner
          </button>
        </div>
      </section>
    </div>
  );
};
