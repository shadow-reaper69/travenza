from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.database import get_db
from app.core.auth import (
    get_password_hash, verify_password, create_access_token,
    get_current_user_required, get_current_user_optional
)
from app.models.models import (
    User, Destination, Interest, TravelType, Attraction,
    LocalService, CultureGuide, SafetyInfo, EmergencyContact,
    Trip, ItineraryDay, ItineraryItem
)
from app.schemas.schemas import (
    UserRegister, UserLogin, TokenResponse, UserResponse,
    DestinationBrief, DestinationDetail, InterestOut, TravelTypeOut,
    TripGenerateRequest, TripResponse, StandardResponse, BudgetBreakdown
)
from app.services.ai_service import AIService

router = APIRouter()

# ----------------- AUTHENTICATION -----------------

@router.post("/auth/register")
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        return {"success": False, "error": {"code": "USER_EXISTS", "message": "Email already registered."}}
    
    hashed = get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        hashed_password=hashed,
        full_name=user_data.full_name
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(data={"sub": str(user.id), "email": user.email})
    return {
        "success": True,
        "data": {
            "access_token": token,
            "token_type": "bearer",
            "user": {"id": user.id, "email": user.email, "full_name": user.full_name}
        }
    }

@router.post("/auth/login")
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        return {"success": False, "error": {"code": "INVALID_CREDENTIALS", "message": "Invalid email or password."}}

    token = create_access_token(data={"sub": str(user.id), "email": user.email})
    return {
        "success": True,
        "data": {
            "access_token": token,
            "token_type": "bearer",
            "user": {"id": user.id, "email": user.email, "full_name": user.full_name}
        }
    }

@router.get("/auth/me")
def get_me(user: User = Depends(get_current_user_required)):
    return {
        "success": True,
        "data": {"id": user.id, "email": user.email, "full_name": user.full_name}
    }

# ----------------- REFERENCE DATA -----------------

@router.get("/reference/interests")
def get_interests(db: Session = Depends(get_db)):
    items = db.query(Interest).all()
    return {"success": True, "data": [InterestOut.from_orm(i) for i in items]}

@router.get("/reference/travel-types")
def get_travel_types(db: Session = Depends(get_db)):
    items = db.query(TravelType).all()
    return {"success": True, "data": [TravelTypeOut.from_orm(t) for t in items]}

# ----------------- DESTINATIONS -----------------

@router.get("/destinations")
def get_destinations(
    query: Optional[str] = None,
    travel_type: Optional[str] = None,
    interest: Optional[str] = None,
    featured_only: bool = False,
    db: Session = Depends(get_db)
):
    q = db.query(Destination)

    if featured_only:
        q = q.filter(Destination.is_featured == True)

    if query:
        search_pattern = f"%{query}%"
        q = q.filter(
            or_(
                Destination.name.ilike(search_pattern),
                Destination.tagline.ilike(search_pattern),
                Destination.description.ilike(search_pattern)
            )
        )

    results = q.all()
    out = []
    for d in results:
        # Check filters
        d_tt_names = [tt.name.lower() for tt in d.travel_types]
        d_int_names = [it.name.lower() for it in d.interests]

        if travel_type and travel_type.lower() not in d_tt_names:
            continue
        if interest and interest.lower() not in d_int_names:
            continue

        out.append({
            "id": d.id,
            "name": d.name,
            "country_name": d.country.name if d.country else "Global",
            "currency": d.currency,
            "tagline": d.tagline,
            "hero_image": d.hero_image,
            "thumbnail": d.thumbnail,
            "approx_daily_budget": d.approx_daily_budget,
            "best_time_to_visit": d.best_time_to_visit,
            "is_featured": d.is_featured,
            "trending_score": d.trending_score,
            "interests": [it.name for it in d.interests],
            "travel_types": [tt.name for tt in d.travel_types]
        })

    return {"success": True, "data": out}

@router.get("/destinations/{dest_id}")
def get_destination_detail(dest_id: int, db: Session = Depends(get_db)):
    dest = db.query(Destination).filter(Destination.id == dest_id).first()
    if not dest:
        return {"success": False, "error": {"code": "DESTINATION_NOT_FOUND", "message": "Destination not found."}}

    return {
        "success": True,
        "data": {
            "id": dest.id,
            "name": dest.name,
            "country_name": dest.country.name if dest.country else "Global",
            "currency": dest.currency,
            "tagline": dest.tagline,
            "description": dest.description,
            "hero_image": dest.hero_image,
            "thumbnail": dest.thumbnail,
            "approx_daily_budget": dest.approx_daily_budget,
            "best_time_to_visit": dest.best_time_to_visit,
            "is_featured": dest.is_featured,
            "trending_score": dest.trending_score,
            "interests": [it.name for it in dest.interests],
            "travel_types": [tt.name for tt in dest.travel_types],
            "attractions": [
                {
                    "id": a.id,
                    "name": a.name,
                    "category": a.category,
                    "description": a.description,
                    "estimated_duration_hours": a.estimated_duration_hours,
                    "estimated_cost": a.estimated_cost,
                    "best_time_of_day": a.best_time_of_day,
                    "location_area": a.location_area
                } for a in dest.attractions
            ],
            "local_services": [
                {
                    "id": s.id,
                    "category": s.category,
                    "name": s.name,
                    "purpose": s.purpose,
                    "platform": s.platform,
                    "app_link": s.app_link,
                    "explanation": s.explanation,
                    "recommended": s.recommended
                } for s in dest.local_services
            ],
            "culture_guides": [
                {
                    "id": c.id,
                    "category": c.category,
                    "title": c.title,
                    "description": c.description,
                    "importance_level": c.importance_level
                } for c in dest.culture_guides
            ],
            "safety_info": [
                {
                    "id": si.id,
                    "title": si.title,
                    "category": si.category,
                    "description": si.description,
                    "severity": si.severity
                } for si in dest.safety_info
            ],
            "emergency_contacts": [
                {
                    "id": ec.id,
                    "service_type": ec.service_type,
                    "contact_number": ec.contact_number,
                    "notes": ec.notes
                } for ec in dest.emergency_contacts
            ]
        }
    }

# ----------------- SMART TRIP PLANNING & ITINERARY -----------------

@router.post("/trips/generate")
def generate_trip(
    req: TripGenerateRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    destination = db.query(Destination).filter(Destination.id == req.destination_id).first()
    if not destination:
        return {"success": False, "error": {"code": "DESTINATION_NOT_FOUND", "message": "Destination not found."}}

    # 1. AI Engine calculates dynamic budget breakdown
    budget = AIService.calculate_budget(destination, req)

    # 2. AI Engine constructs day-by-day itinerary
    itinerary_days_data = AIService.generate_itinerary(destination, req)

    # 3. Create or preview Trip
    trip = Trip(
        user_id=current_user.id if current_user else None,
        destination_id=destination.id,
        title=f"{destination.name} with {req.travel_type}",
        travel_type=req.travel_type,
        num_travellers=req.num_travellers,
        duration_days=req.duration_days,
        start_date=req.start_date,
        end_date=req.end_date,
        budget_tier=req.budget_tier,
        budget_total=budget.total,
        currency=destination.currency or "USD",
        pace_preference=req.pace_preference,
        interests=req.interests,
        preferences={"notes": req.additional_notes},
        summary=f"Personalized {req.duration_days}-day {req.travel_type} itinerary exploring {destination.name}. Curated for a {req.budget_tier.lower()} budget with a {req.pace_preference.lower()} tempo."
    )
    db.add(trip)
    db.flush()

    # Save Days and Items
    for d_data in itinerary_days_data:
        day_record = ItineraryDay(
            trip_id=trip.id,
            day_number=d_data.day_number,
            theme=d_data.theme,
            overview=d_data.overview,
            estimated_day_cost=d_data.estimated_day_cost
        )
        db.add(day_record)
        db.flush()

        for item_data in d_data.items:
            item_record = ItineraryItem(
                day_id=day_record.id,
                time_slot=item_data.time_slot,
                title=item_data.title,
                category=item_data.category,
                description=item_data.description,
                why_this=item_data.why_this,
                estimated_duration_hours=item_data.estimated_duration_hours,
                estimated_cost=item_data.estimated_cost,
                travel_time_from_prev=item_data.travel_time_from_prev,
                location_name=item_data.location_name
            )
            db.add(item_record)

    db.commit()
    db.refresh(trip)

    return {
        "success": True,
        "data": {
            "trip_id": trip.id,
            "title": trip.title,
            "destination_id": destination.id,
            "destination_name": destination.name,
            "country_name": destination.country.name if destination.country else "",
            "travel_type": trip.travel_type,
            "num_travellers": trip.num_travellers,
            "duration_days": trip.duration_days,
            "start_date": trip.start_date,
            "end_date": trip.end_date,
            "budget_tier": trip.budget_tier,
            "budget_total": trip.budget_total,
            "currency": trip.currency,
            "pace_preference": trip.pace_preference,
            "interests": trip.interests,
            "summary": trip.summary,
            "budget_breakdown": budget.dict(),
            "itinerary_days": [
                {
                    "day_number": d.day_number,
                    "theme": d.theme,
                    "overview": d.overview,
                    "estimated_day_cost": d.estimated_day_cost,
                    "items": [
                        {
                            "time_slot": it.time_slot,
                            "title": it.title,
                            "category": it.category,
                            "description": it.description,
                            "why_this": it.why_this,
                            "estimated_duration_hours": it.estimated_duration_hours,
                            "estimated_cost": it.estimated_cost,
                            "travel_time_from_prev": it.travel_time_from_prev,
                            "location_name": it.location_name
                        } for it in d.items
                    ]
                } for d in trip.itinerary_days
            ]
        }
    }

@router.get("/trips/{trip_id}")
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        return {"success": False, "error": {"code": "TRIP_NOT_FOUND", "message": "Trip not found."}}

    dest = trip.destination
    # Recompute budget distribution
    req_dummy = TripGenerateRequest(
        destination_id=trip.destination_id,
        travel_type=trip.travel_type,
        num_travellers=trip.num_travellers,
        duration_days=trip.duration_days,
        budget_tier=trip.budget_tier,
        interests=trip.interests or []
    )
    budget = AIService.calculate_budget(dest, req_dummy)

    return {
        "success": True,
        "data": {
            "id": trip.id,
            "title": trip.title,
            "destination_id": dest.id,
            "destination_name": dest.name,
            "country_name": dest.country.name if dest.country else "",
            "travel_type": trip.travel_type,
            "num_travellers": trip.num_travellers,
            "duration_days": trip.duration_days,
            "start_date": trip.start_date,
            "end_date": trip.end_date,
            "budget_tier": trip.budget_tier,
            "budget_total": trip.budget_total,
            "currency": trip.currency,
            "pace_preference": trip.pace_preference,
            "interests": trip.interests,
            "summary": trip.summary,
            "budget_breakdown": budget.dict(),
            "itinerary_days": [
                {
                    "day_number": d.day_number,
                    "theme": d.theme,
                    "overview": d.overview,
                    "estimated_day_cost": d.estimated_day_cost,
                    "items": [
                        {
                            "time_slot": it.time_slot,
                            "title": it.title,
                            "category": it.category,
                            "description": it.description,
                            "why_this": it.why_this,
                            "estimated_duration_hours": it.estimated_duration_hours,
                            "estimated_cost": it.estimated_cost,
                            "travel_time_from_prev": it.travel_time_from_prev,
                            "location_name": it.location_name
                        } for it in d.items
                    ]
                } for d in sorted(trip.itinerary_days, key=lambda x: x.day_number)
            ]
        }
    }

@router.get("/saved-trips")
def list_saved_trips(
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    if current_user:
        trips = db.query(Trip).filter(Trip.user_id == current_user.id).order_by(Trip.created_at.desc()).all()
    else:
        # Return recent guest trips
        trips = db.query(Trip).order_by(Trip.created_at.desc()).limit(10).all()

    out = []
    for t in trips:
        out.append({
            "id": t.id,
            "title": t.title,
            "destination_name": t.destination.name,
            "country_name": t.destination.country.name if t.destination.country else "",
            "destination_thumbnail": t.destination.thumbnail or t.destination.hero_image,
            "travel_type": t.travel_type,
            "duration_days": t.duration_days,
            "num_travellers": t.num_travellers,
            "budget_total": t.budget_total,
            "currency": t.currency,
            "budget_tier": t.budget_tier,
            "created_at": t.created_at.isoformat() if t.created_at else None
        })

    return {"success": True, "data": out}

@router.delete("/trips/{trip_id}")
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        return {"success": False, "error": {"code": "NOT_FOUND", "message": "Trip not found"}}
    db.delete(trip)
    db.commit()
    return {"success": True, "data": {"deleted": True}}
