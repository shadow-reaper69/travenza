import React, { useState } from 'react';
import { X, Lock, Mail, User, AlertCircle, Loader2 } from 'lucide-react';
import { api } from '../services/api';
import { User as UserType } from '../types';

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (user: UserType) => void;
}

export const AuthModal: React.FC<AuthModalProps> = ({ isOpen, onClose, onSuccess }) => {
  const [isRegister, setIsRegister] = useState<boolean>(false);
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [fullName, setFullName] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      if (isRegister) {
        const res = await api.register(email, password, fullName);
        if (res) {
          onSuccess(res.user);
          onClose();
        } else {
          setError('Registration failed. Email might already exist.');
        }
      } else {
        const res = await api.login(email, password);
        if (res) {
          onSuccess(res.user);
          onClose();
        } else {
          setError('Invalid email or password.');
        }
      }
    } catch {
      setError('An error occurred during authentication.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-primary-text/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white rounded-3xl p-6 sm:p-8 max-w-md w-full border border-border shadow-premium relative space-y-6">
        <button
          onClick={onClose}
          className="absolute top-6 right-6 p-2 text-secondary-text hover:text-primary-text rounded-full hover:bg-surface-subtle"
        >
          <X className="w-5 h-5" />
        </button>

        <div>
          <span className="text-[11px] font-bold text-peach-dark uppercase tracking-widest block mb-1">
            Travenza Account
          </span>
          <h2 className="text-2xl font-bold text-primary-text">
            {isRegister ? 'Create Your Account' : 'Welcome Back'}
          </h2>
          <p className="text-xs text-secondary-text mt-1">
            {isRegister
              ? 'Save personal itineraries, emergency notes, and offline guides.'
              : 'Sign in to access your saved trips and travel dashboards.'}
          </p>
        </div>

        {error && (
          <div className="p-3 rounded-xl bg-rose-50 border border-rose-200 text-xs text-rose-700 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {isRegister && (
            <div>
              <label className="text-xs font-semibold text-primary-text block mb-1">Full Name</label>
              <div className="relative">
                <User className="w-4 h-4 text-secondary-text absolute left-4 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  required
                  placeholder="e.g. Alex Morgan"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="w-full pl-11 pr-4 py-3 rounded-xl border border-border text-xs focus:outline-none focus:ring-1 focus:ring-peach bg-surface-subtle/50"
                />
              </div>
            </div>
          )}

          <div>
            <label className="text-xs font-semibold text-primary-text block mb-1">Email Address</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-secondary-text absolute left-4 top-1/2 -translate-y-1/2" />
              <input
                type="email"
                required
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full pl-11 pr-4 py-3 rounded-xl border border-border text-xs focus:outline-none focus:ring-1 focus:ring-peach bg-surface-subtle/50"
              />
            </div>
          </div>

          <div>
            <label className="text-xs font-semibold text-primary-text block mb-1">Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-secondary-text absolute left-4 top-1/2 -translate-y-1/2" />
              <input
                type="password"
                required
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full pl-11 pr-4 py-3 rounded-xl border border-border text-xs focus:outline-none focus:ring-1 focus:ring-peach bg-surface-subtle/50"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 rounded-xl bg-peach hover:bg-peach-dark text-white font-medium text-xs shadow-soft transition-all flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {loading && <Loader2 className="w-4 h-4 animate-spin" />}
            <span>{isRegister ? 'Create Account' : 'Sign In'}</span>
          </button>
        </form>

        <div className="pt-2 text-center text-xs text-secondary-text">
          {isRegister ? (
            <span>
              Already have an account?{' '}
              <button
                onClick={() => { setIsRegister(false); setError(null); }}
                className="font-bold text-peach-dark hover:underline"
              >
                Sign In
              </button>
            </span>
          ) : (
            <span>
              Don't have an account?{' '}
              <button
                onClick={() => { setIsRegister(true); setError(null); }}
                className="font-bold text-peach-dark hover:underline"
              >
                Create Account
              </button>
            </span>
          )}
        </div>
      </div>
    </div>
  );
};
