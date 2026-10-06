# TRAVENZA — AGENTS & ENGINEERING GUIDELINES

## Project Overview
Travenza is a modern AI-powered smart travel companion providing seamless trip planning, personalized day-wise itineraries, local essentials (transport, food delivery, payments, eSIM/sim, maps), cultural etiquette (Do's & Don'ts, phrases), safety center (emergency contacts, scams, alerts), and dynamic budget breakdowns.

## Tech Stack
- **Backend**: FastAPI, SQLAlchemy (SQLite/PostgreSQL compatible), Pydantic v2, PyJWT, Passlib (bcrypt), Uvicorn.
- **Frontend**: React 18 / Vite, TypeScript, Tailwind CSS, Lucide Icons.
- **Theme & Aesthetics**: Editorial travel aesthetic. Palette: White (#FFFFFF), Canvas/Bg (#FAFAF9), Neutral dark (#171717), Subtle border (#E7E5E4), Peach accent (#F4A58A), Light peach tint (#FCE7DE), Dark peach (#D98268).

## Architectural Conventions
- **Clean Service-Layer Architecture**: Keep API route controllers thin; business calculations and AI orchestrations live in `services/`.
- **Database Schema**: Unified relational models for Destinations, Attractions, Local Services, Culture Guides, Safety Info, Trips, and Itinerary items.
- **Security First**: JWT tokens, bcrypt password hashing, standard error handling schemas (`{success: true, data: ...}` / `{success: false, error: ...}`).
- **Strict Typing**: Full TypeScript interfaces matching backend Pydantic models.
