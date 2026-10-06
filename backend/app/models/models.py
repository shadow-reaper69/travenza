import datetime
from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

# Association table for Destination and Interests
destination_interests = Table(
    "destination_interests",
    Base.metadata,
    Column("destination_id", Integer, ForeignKey("destinations.id", ondelete="CASCADE"), primary_key=True),
    Column("interest_id", Integer, ForeignKey("interests.id", ondelete="CASCADE"), primary_key=True)
)

# Association table for Destination and TravelTypes
destination_travel_types = Table(
    "destination_travel_types",
    Base.metadata,
    Column("destination_id", Integer, ForeignKey("destinations.id", ondelete="CASCADE"), primary_key=True),
    Column("travel_type_id", Integer, ForeignKey("travel_types.id", ondelete="CASCADE"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    trips = relationship("Trip", back_populates="user", cascade="all, delete-orphan")

class Interest(Base):
    __tablename__ = "interests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    icon = Column(String(50), nullable=True)
    description = Column(String(255), nullable=True)

class TravelType(Base):
    __tablename__ = "travel_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    tagline = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(10), unique=True, nullable=False)
    currency_code = Column(String(10), default="USD")
    currency_symbol = Column(String(10), default="$")
    flag_emoji = Column(String(10), nullable=True)

    destinations = relationship("Destination", back_populates="country")

class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    tagline = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    hero_image = Column(String(500), nullable=True)
    thumbnail = Column(String(500), nullable=True)
    approx_daily_budget = Column(Float, default=100.0)  # in destination native or USD
    currency = Column(String(10), default="USD")
    best_time_to_visit = Column(String(100), nullable=True)
    is_featured = Column(Boolean, default=False)
    trending_score = Column(Integer, default=0)

    country = relationship("Country", back_populates="destinations")
    interests = relationship("Interest", secondary=destination_interests)
    travel_types = relationship("TravelType", secondary=destination_travel_types)
    attractions = relationship("Attraction", back_populates="destination", cascade="all, delete-orphan")
    local_services = relationship("LocalService", back_populates="destination", cascade="all, delete-orphan")
    culture_guides = relationship("CultureGuide", back_populates="destination", cascade="all, delete-orphan")
    safety_info = relationship("SafetyInfo", back_populates="destination", cascade="all, delete-orphan")
    emergency_contacts = relationship("EmergencyContact", back_populates="destination", cascade="all, delete-orphan")

class Attraction(Base):
    __tablename__ = "attractions"

    id = Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=True) # Heritage, Nature, Viewpoint, Culinary, etc.
    description = Column(Text, nullable=False)
    estimated_duration_hours = Column(Float, default=2.0)
    estimated_cost = Column(Float, default=0.0)
    best_time_of_day = Column(String(50), nullable=True) # Morning, Afternoon, Evening
    location_area = Column(String(100), nullable=True)
    image_url = Column(String(500), nullable=True)

    destination = relationship("Destination", back_populates="attractions")

class LocalService(Base):
    __tablename__ = "local_services"

    id = Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    category = Column(String(50), nullable=False) # Getting Around, Food Delivery, Payments, eSIM & SIM, Navigation
    name = Column(String(100), nullable=False)
    purpose = Column(String(200), nullable=False)
    platform = Column(String(100), default="iOS / Android")
    app_link = Column(String(255), nullable=True)
    explanation = Column(Text, nullable=False)
    recommended = Column(Boolean, default=True)

    destination = relationship("Destination", back_populates="local_services")

class CultureGuide(Base):
    __tablename__ = "culture_guides"

    id = Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    category = Column(String(50), nullable=False) # DO, DONT, Etiquette, Dress, Photography, Religion, Tipping, Greetings, Useful Phrases
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    importance_level = Column(String(20), default="Standard") # Crucial, High, Standard

    destination = relationship("Destination", back_populates="culture_guides")

class SafetyInfo(Base):
    __tablename__ = "safety_information"

    id = Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    title = Column(String(200), nullable=False)
    category = Column(String(50), default="General") # General Safety, Scam Awareness, Night Safety, Water/Food, Solo Travel Note
    description = Column(Text, nullable=False)
    severity = Column(String(20), default="Notice") # Warning, Notice, Advisory

    destination = relationship("Destination", back_populates="safety_info")

class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"

    id = Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    service_type = Column(String(100), nullable=False) # Police, Ambulance, Fire, Tourist Assistance Helpline, General Emergency
    contact_number = Column(String(50), nullable=False)
    notes = Column(String(255), nullable=True)

    destination = relationship("Destination", back_populates="emergency_contacts")

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    title = Column(String(200), nullable=False)
    travel_type = Column(String(50), nullable=False)
    num_travellers = Column(Integer, default=1)
    duration_days = Column(Integer, default=3)
    start_date = Column(String(50), nullable=True)
    end_date = Column(String(50), nullable=True)
    budget_tier = Column(String(50), default="Comfort") # Budget, Comfort, Premium, Luxury
    budget_total = Column(Float, default=0.0)
    currency = Column(String(10), default="USD")
    pace_preference = Column(String(50), default="Balanced") # Relaxed, Balanced, Packed
    interests = Column(JSON, default=list)
    preferences = Column(JSON, default=dict)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="trips")
    destination = relationship("Destination")
    itinerary_days = relationship("ItineraryDay", back_populates="trip", cascade="all, delete-orphan")

class ItineraryDay(Base):
    __tablename__ = "itinerary_days"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    day_number = Column(Integer, nullable=False)
    theme = Column(String(200), nullable=False)
    overview = Column(Text, nullable=True)
    estimated_day_cost = Column(Float, default=0.0)

    trip = relationship("Trip", back_populates="itinerary_days")
    items = relationship("ItineraryItem", back_populates="day", cascade="all, delete-orphan")

class ItineraryItem(Base):
    __tablename__ = "itinerary_items"

    id = Column(Integer, primary_key=True, index=True)
    day_id = Column(Integer, ForeignKey("itinerary_days.id"), nullable=False)
    time_slot = Column(String(20), nullable=False) # e.g. "09:00", "13:00"
    title = Column(String(200), nullable=False)
    category = Column(String(50), nullable=True) # Attraction, Dining, Viewpoint, Activity, Leisure
    description = Column(Text, nullable=False)
    why_this = Column(Text, nullable=True)
    estimated_duration_hours = Column(Float, default=1.5)
    estimated_cost = Column(Float, default=0.0)
    travel_time_from_prev = Column(String(50), nullable=True) # e.g. "15 mins via Metro"
    location_name = Column(String(150), nullable=True)

    day = relationship("ItineraryDay", back_populates="items")
