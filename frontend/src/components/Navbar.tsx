import React from 'react';
import { Compass, BookmarkCheck, User as UserIcon, Shield, Sparkles, MapPin, Menu, X } from 'lucide-react';
import { User } from '../types';

interface NavbarProps {
  currentView: string;
  setCurrentView: (view: string) => void;
  currentUser: User | null;
  onOpenAuth: () => void;
  onLogout: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentView,
  setCurrentView,
  currentUser,
  onOpenAuth,
  onLogout
}) => {
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);

  const navLinks = [
    { id: 'landing', label: 'Home' },
    { id: 'explore', label: 'Explore Destinations' },
    { id: 'planner', label: 'Plan a Trip' },
    { id: 'saved', label: 'Saved Trips' },
  ];

  return (
    <header className="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        {/* Brand Logo */}
        <div 
          onClick={() => setCurrentView('landing')} 
          className="flex items-center gap-3 cursor-pointer group"
        >
          <div className="w-10 h-10 rounded-xl bg-peach flex items-center justify-center text-white font-bold text-xl shadow-soft group-hover:scale-105 transition-transform duration-200">
            T
          </div>
          <div>
            <span className="text-xl font-bold tracking-tight text-primary-text block">TRAVENZA</span>
            <span className="text-[10px] uppercase tracking-widest text-secondary-text font-medium block -mt-1">
              Smart Travel Companion
            </span>
          </div>
        </div>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center gap-1">
          {navLinks.map((link) => (
            <button
              key={link.id}
              onClick={() => setCurrentView(link.id)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 ${
                currentView === link.id
                  ? 'bg-surface-subtle text-primary-text shadow-sm'
                  : 'text-secondary-text hover:text-primary-text hover:bg-surface-subtle/50'
              }`}
            >
              {link.label}
            </button>
          ))}
        </nav>

        {/* Action Controls */}
        <div className="hidden md:flex items-center gap-3">
          {currentUser ? (
            <div className="flex items-center gap-3 bg-surface-subtle px-3 py-1.5 rounded-full border border-border">
              <div className="w-7 h-7 rounded-full bg-peach-light text-peach-dark flex items-center justify-center text-xs font-semibold">
                {currentUser.full_name ? currentUser.full_name.charAt(0).toUpperCase() : 'U'}
              </div>
              <span className="text-sm font-medium text-primary-text max-w-[120px] truncate">
                {currentUser.full_name || currentUser.email}
              </span>
              <button
                onClick={onLogout}
                className="text-xs text-secondary-text hover:text-peach-dark transition-colors ml-1"
              >
                Sign out
              </button>
            </div>
          ) : (
            <button
              onClick={onOpenAuth}
              className="text-sm font-medium text-primary-text hover:text-peach-dark px-3 py-2 transition-colors"
            >
              Sign In
            </button>
          )}

          <button
            onClick={() => setCurrentView('planner')}
            className="flex items-center gap-2 bg-peach hover:bg-peach-dark text-white px-5 py-2.5 rounded-full text-sm font-medium shadow-soft hover:shadow-premium transition-all duration-200"
          >
            <Sparkles className="w-4 h-4" />
            <span>Plan My Trip</span>
          </button>
        </div>

        {/* Mobile Hamburger */}
        <div className="md:hidden flex items-center">
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-2 text-secondary-text hover:text-primary-text"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b border-border bg-white px-4 pt-2 pb-6 space-y-2">
          {navLinks.map((link) => (
            <button
              key={link.id}
              onClick={() => {
                setCurrentView(link.id);
                setMobileMenuOpen(false);
              }}
              className="block w-full text-left px-4 py-3 rounded-lg text-base font-medium text-primary-text hover:bg-surface-subtle"
            >
              {link.label}
            </button>
          ))}
          <div className="pt-4 border-t border-border flex flex-col gap-2">
            {currentUser ? (
              <div className="flex items-center justify-between px-4 py-2">
                <span className="text-sm text-secondary-text">{currentUser.email}</span>
                <button onClick={onLogout} className="text-sm text-peach-dark font-medium">Sign Out</button>
              </div>
            ) : (
              <button
                onClick={() => {
                  onOpenAuth();
                  setMobileMenuOpen(false);
                }}
                className="w-full text-center py-2.5 rounded-lg border border-border text-sm font-medium"
              >
                Sign In
              </button>
            )}
            <button
              onClick={() => {
                setCurrentView('planner');
                setMobileMenuOpen(false);
              }}
              className="w-full py-3 rounded-full bg-peach text-white font-medium text-center shadow-soft"
            >
              Plan My Trip
            </button>
          </div>
        </div>
      )}
    </header>
  );
};
