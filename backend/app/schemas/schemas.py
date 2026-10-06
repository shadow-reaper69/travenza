from typing import List, Optional, Any, Dict
from pydantic import BaseModel, EmailStr

# Auth Schemas
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# Reference Schemas
class InterestOut(BaseModel):
    id: int
    name: str
    slug: str
    icon: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True

class TravelTypeOut(BaseModel):
    id: int
    name: str
    slug: str
    tagline: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None

    class Config:
        from_attributes = True

class AttractionOut(BaseModel):
    id: int
    name: str
    category: Optional[str] = None
    description: str
    estimated_duration_hours: float
    estimated_cost: float
    best_time_of_day: Optional[str] = None
    location_area: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True

class LocalServiceOut(BaseModel):
    id: int
    category: str
    name: str
    purpose: str
    platform: str
    app_link: Optional[str] = None
    explanation: str
    recommended: bool

    class Config:
        from_attributes = True

class CultureGuideOut(BaseModel):
    id: int
    category: str
    title: str
    description: str
    importance_level: str

    class Config:
        from_attributes = True

class SafetyInfoOut(BaseModel):
    id: int
    title: str
    category: str
    description: str
    severity: str

    class Config:
        from_attributes = True

class EmergencyContactOut(BaseModel):
    id: int
    service_type: str
    contact_number: str
    notes: Optional[str] = None

    class Config:
        from_attributes = True

class DestinationBrief(BaseModel):
    id: int
    name: str
    country_name: str
    currency: str
    tagline: Optional[str] = None
    hero_image: Optional[str] = None
    thumbnail: Optional[str] = None
    approx_daily_budget: float
    best_time_to_visit: Optional[str] = None
    is_featured: bool
    trending_score: int
    interests: List[str] = []
    travel_types: List[str] = []

    class Config:
        from_attributes = True

class DestinationDetail(DestinationBrief):
    description: str
    attractions: List[AttractionOut] = []
    local_services: List[LocalServiceOut] = []
    culture_guides: List[CultureGuideOut] = []
    safety_info: List[SafetyInfoOut] = []
    emergency_contacts: List[EmergencyContactOut] = []

# Trip Generator & Itinerary Schemas
class TripGenerateRequest(BaseModel):
    destination_id: int
    travel_type: str # e.g. "Solo", "Friends", "Family", "Couple", "Honeymoon", "Senior Citizens", "Business", "Group Tour"
    num_travellers: int = 1
    duration_days: int = 3
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    budget_tier: str = "Comfort" # "Budget", "Comfort", "Premium", "Luxury"
    interests: List[str] = []
    pace_preference: str = "Balanced" # "Relaxed", "Balanced", "Packed"
    additional_notes: Optional[str] = None

class ItineraryItemOut(BaseModel):
    id: Optional[int] = None
    time_slot: str
    title: str
    category: Optional[str] = None
    description: str
    why_this: Optional[str] = None
    estimated_duration_hours: float
    estimated_cost: float
    travel_time_from_prev: Optional[str] = None
    location_name: Optional[str] = None

    class Config:
        from_attributes = True

class ItineraryDayOut(BaseModel):
    id: Optional[int] = None
    day_number: int
    theme: str
    overview: Optional[str] = None
    estimated_day_cost: float
    items: List[ItineraryItemOut] = []

    class Config:
        from_attributes = True

class BudgetBreakdown(BaseModel):
    accommodation: float
    food: float
    transportation: float
    activities: float
    shopping_misc: float
    total: float
    per_person: float
    currency: str

class TripResponse(BaseModel):
    id: int
    title: str
    destination_id: int
    destination_name: str
    country_name: str
    travel_type: str
    num_travellers: int
    duration_days: int
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    budget_tier: str
    budget_total: float
    currency: str
    pace_preference: str
    interests: List[str]
    summary: Optional[str] = None
    itinerary_days: List[ItineraryDayOut] = []
    budget_breakdown: Optional[BudgetBreakdown] = None
    created_at: Any = None

    class Config:
        from_attributes = True

class StandardResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
