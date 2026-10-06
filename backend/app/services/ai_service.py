import math
from typing import List, Dict, Any
from app.models.models import Destination, Attraction
from app.schemas.schemas import TripGenerateRequest, ItineraryDayOut, ItineraryItemOut, BudgetBreakdown

class AIService:
    """
    Intelligent Itinerary Generator & Recommendation Engine.
    Structures verified destination data, adapts pacing to travel persona,
    calculates real-world budget distributions, and outputs actionable schedules.
    """

    @classmethod
    def calculate_budget(cls, destination: Destination, req: TripGenerateRequest) -> BudgetBreakdown:
        base_daily = destination.approx_daily_budget or 100.0

        # Multiplier according to tier
        tier_multipliers = {
            "Budget": 0.65,
            "Comfort": 1.0,
            "Premium": 1.85,
            "Luxury": 3.2
        }
        multiplier = tier_multipliers.get(req.budget_tier, 1.0)
        daily_per_person = base_daily * multiplier

        # Group economics (accommodation shared if couples/friends/family)
        num = max(1, req.num_travellers)
        days = max(1, req.duration_days)

        # Persona cost adjustments
        if req.travel_type in ["Couple", "Honeymoon"]:
            hotel_ratio = 0.42
            food_ratio = 0.28
            activity_ratio = 0.18
            transport_ratio = 0.12
        elif req.travel_type in ["Friends", "Solo"]:
            hotel_ratio = 0.30
            food_ratio = 0.30
            activity_ratio = 0.25
            transport_ratio = 0.15
        elif req.travel_type == "Family":
            hotel_ratio = 0.45
            food_ratio = 0.25
            activity_ratio = 0.18
            transport_ratio = 0.12
        else:
            hotel_ratio = 0.35
            food_ratio = 0.28
            activity_ratio = 0.22
            transport_ratio = 0.15

        total_base = daily_per_person * days * num

        # Calculate breakdown
        accommodation = round(total_base * hotel_ratio, 2)
        food = round(total_base * food_ratio, 2)
        transportation = round(total_base * transport_ratio, 2)
        activities = round(total_base * activity_ratio, 2)
        shopping_misc = round(total_base * 0.10, 2)
        total = accommodation + food + transportation + activities + shopping_misc
        per_person = round(total / num, 2)

        return BudgetBreakdown(
            accommodation=accommodation,
            food=food,
            transportation=transportation,
            activities=activities,
            shopping_misc=shopping_misc,
            total=total,
            per_person=per_person,
            currency=destination.currency or "USD"
        )

    @classmethod
    def generate_itinerary(cls, destination: Destination, req: TripGenerateRequest) -> List[ItineraryDayOut]:
        attractions: List[Attraction] = destination.attractions or []
        days_count = max(1, min(req.duration_days, 14))
        interests_lower = [i.lower() for i in req.interests]
        
        # Pacing configuration
        is_relaxed = req.pace_preference == "Relaxed"
        is_packed = req.pace_preference == "Packed"

        # Prioritize attractions matching interests
        sorted_attractions = sorted(
            attractions,
            key=lambda a: any(i in (a.category or "").lower() for i in interests_lower),
            reverse=True
        )

        day_themes = [
            f"Arrival, Heritage & Orienting in {destination.name}",
            f"Cultural Wonders & Architectural Highlights",
            f"Scenic Nature, Hidden Corners & Local Gastronomy",
            f"Vibrant Neighborhoods & Panoramic Vistas",
            f"Artisan Markets, Coastal Walks & Sunset Relaxation",
            f"Off-The-Beaten-Path Treasures & Day Excursions",
            f"Farewell Moments, Leisurely Souvenirs & Sunset"
        ]

        itinerary_days: List[ItineraryDayOut] = []

        attr_index = 0
        total_attrs = len(sorted_attractions)

        for day_num in range(1, days_count + 1):
            theme = day_themes[(day_num - 1) % len(day_themes)]
            items: List[ItineraryItemOut] = []
            day_cost = 0.0

            # 1. Morning slot
            if attr_index < total_attrs:
                attr = sorted_attractions[attr_index % total_attrs]
                attr_index += 1
                morning_cost = attr.estimated_cost
                day_cost += morning_cost
                items.append(ItineraryItemOut(
                    time_slot="09:00 AM",
                    title=f"Explore {attr.name}",
                    category=attr.category or "Attraction",
                    description=attr.description,
                    why_this=f"Perfect for {req.travel_type} travellers looking to experience authentic local {attr.category or 'culture'}.",
                    estimated_duration_hours=attr.estimated_duration_hours or 2.0,
                    estimated_cost=morning_cost,
                    travel_time_from_prev="Starting from accommodation",
                    location_name=attr.location_area or destination.name
                ))
            else:
                items.append(ItineraryItemOut(
                    time_slot="09:30 AM",
                    title=f"Morning Stroll through {destination.name} Heritage Alleys",
                    category="Culture",
                    description=f"Leisurely walk through historic local quarters and landmark coffee stops.",
                    why_this="Gentle morning discovery pace.",
                    estimated_duration_hours=1.5,
                    estimated_cost=200 if destination.currency == "INR" else 15,
                    travel_time_from_prev="10 mins transit",
                    location_name=destination.name
                ))

            # 2. Midday Lunch
            lunch_cost = 600 if destination.currency == "INR" else 25
            day_cost += lunch_cost
            items.append(ItineraryItemOut(
                time_slot="01:00 PM",
                title=f"Authentic {destination.name} Culinary Tasting",
                category="Dining",
                description=f"Enjoy regional specialties and signature local recipes at a recommended neighborhood bistro.",
                why_this="Indulge in destination food culture tailored to your preferences.",
                estimated_duration_hours=1.5,
                estimated_cost=lunch_cost,
                travel_time_from_prev="Short walk from morning sight",
                location_name="Central District"
            ))

            # 3. Afternoon slot
            if not is_relaxed or (day_num % 2 == 1):
                if attr_index < total_attrs:
                    attr2 = sorted_attractions[attr_index % total_attrs]
                    attr_index += 1
                    afternoon_cost = attr2.estimated_cost
                    day_cost += afternoon_cost
                    items.append(ItineraryItemOut(
                        time_slot="03:30 PM",
                        title=f"Visit {attr2.name}",
                        category=attr2.category or "Sightseeing",
                        description=attr2.description,
                        why_this=f"Highly rated {attr2.category} activity tailored to {', '.join(req.interests[:2]) or req.travel_type} travellers.",
                        estimated_duration_hours=attr2.estimated_duration_hours or 2.0,
                        estimated_cost=afternoon_cost,
                        travel_time_from_prev="20 mins via local transit",
                        location_name=attr2.location_area or destination.name
                    ))

            # 4. Evening sunset or leisure
            evening_cost = 400 if destination.currency == "INR" else 20
            day_cost += evening_cost
            items.append(ItineraryItemOut(
                time_slot="06:30 PM",
                title=f"Sunset & Evening Leisure in {destination.name}",
                category="Relaxation",
                description="Unwind at scenic waterfront promenades, rooftop viewpoints, or artisan night markets.",
                why_this="Relaxed conclusion of the day with serene sunset photography opportunities.",
                estimated_duration_hours=2.0,
                estimated_cost=evening_cost,
                travel_time_from_prev="15 mins walk",
                location_name="Scenic Promenade"
            ))

            # If packed pace, add a nighttime experience
            if is_packed:
                night_cost = 800 if destination.currency == "INR" else 35
                day_cost += night_cost
                items.append(ItineraryItemOut(
                    time_slot="09:00 PM",
                    title="Nighttime Atmosphere & Cultural Walk",
                    category="Nightlife",
                    description=f"Experience {destination.name}'s illuminated architectural facades or bustling evening street shacks.",
                    why_this="For energetic travellers maximizing evening hours.",
                    estimated_duration_hours=1.5,
                    estimated_cost=night_cost,
                    travel_time_from_prev="10 mins ride",
                    location_name="Downtown"
                ))

            itinerary_days.append(ItineraryDayOut(
                day_number=day_num,
                theme=theme,
                overview=f"Day {day_num} prioritizes immersive discovery, curated local flavors, and scenic timing.",
                estimated_day_cost=day_cost,
                items=items
            ))

        return itinerary_days
