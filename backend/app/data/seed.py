import json
from sqlalchemy.orm import Session
from app.models.models import (
    Country, Destination, Interest, TravelType, Attraction,
    LocalService, CultureGuide, SafetyInfo, EmergencyContact
)

SEED_DESTINATIONS = [
    {
        "name": "Goa",
        "country": "India",
        "country_code": "IN",
        "currency": "INR",
        "currency_symbol": "₹",
        "tagline": "Golden shores, Portuguese heritage, and vibrant coastal culture",
        "description": "Goa blends serene Arabian sea beaches, 16th-century Portuguese architecture, spice plantations, and lively open-air beach shacks. Perfect for solo travellers, couples, and groups of friends seeking both coastal relaxation and spirited adventures.",
        "hero_image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1600&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=600&q=80",
        "approx_daily_budget": 3500.0,
        "best_time_to_visit": "November to February",
        "is_featured": True,
        "trending_score": 95,
        "travel_types": ["Friends", "Solo", "Couple", "Honeymoon", "Group Tour"],
        "interests": ["Beaches", "Nightlife", "Food", "History", "Relaxation", "Adventure"],
        "attractions": [
            {"name": "Basilica of Bom Jesus", "category": "History", "description": "UNESCO World Heritage Roman Catholic basilica holding the mortal remains of St. Francis Xavier.", "estimated_duration_hours": 1.5, "estimated_cost": 50, "best_time_of_day": "Morning", "location_area": "Old Goa"},
            {"name": "Palolem Beach Sunset Walk", "category": "Beaches", "description": "Crescent-shaped serene beach framed by green coconut palms and gentle warm waves.", "estimated_duration_hours": 2.5, "estimated_cost": 0, "best_time_of_day": "Evening", "location_area": "South Goa"},
            {"name": "Fontainhas Latin Quarter Walking Tour", "category": "Culture", "description": "Vibrant colonial streets painted in cadmium yellow, blue, and terracotta with Portuguese azulejos.", "estimated_duration_hours": 2.0, "estimated_cost": 200, "best_time_of_day": "Morning", "location_area": "Panaji"},
            {"name": "Sahakari Spice Farm Experience", "category": "Nature", "description": "Guided botanical walk through aromatic cardamom, cinnamon, and vanilla groves with traditional Goan lunch.", "estimated_duration_hours": 3.0, "estimated_cost": 600, "best_time_of_day": "Afternoon", "location_area": "Ponda"},
            {"name": "Chapora Fort & Vagator Cliff View", "category": "Viewpoint", "description": "Iconic red-laterite clifftop fortress overlooking the azure Arabian sea and coastline.", "estimated_duration_hours": 1.5, "estimated_cost": 0, "best_time_of_day": "Late Afternoon", "location_area": "North Goa"}
        ],
        "local_services": [
            {"category": "Getting Around", "name": "GoaMiles", "purpose": "State-governed Cab Booking App", "platform": "iOS / Android", "explanation": "Official app for fixed-price taxi rides across North & South Goa without meter disputes.", "app_link": "https://goamiles.com", "recommended": True},
            {"category": "Getting Around", "name": "Self-Drive Scooters / Bike Rentals", "purpose": "Local 2-Wheeler Rental", "platform": "On-Ground Local Desks", "explanation": "Most efficient transport method. Always wear helmets and carry a valid driving license.", "app_link": "", "recommended": True},
            {"category": "Food Delivery", "name": "Swiggy / Zomato", "purpose": "Online Food & Grocery Delivery", "platform": "iOS / Android", "explanation": "Active in Panaji, Margao, Calangute, and major coastal hubs for local Goan seafood and international fare.", "app_link": "https://swiggy.com", "recommended": True},
            {"category": "Payments", "name": "UPI (Google Pay, PhonePe, Paytm)", "purpose": "Instant QR Payments", "platform": "iOS / Android", "explanation": "Accepted virtually everywhere including street shacks, beach stalls, and restaurants.", "app_link": "", "recommended": True},
            {"category": "eSIM & SIM", "name": "Airtel / Jio Travel SIM", "purpose": "High-speed 4G/5G Connectivity", "platform": "Airport Kiosks & City Stores", "explanation": "Jio and Airtel offer highest coastal connectivity coverage. Carry passport and visa for activation.", "app_link": "", "recommended": True},
            {"category": "Navigation", "name": "Google Maps (Offline Download Recommended)", "purpose": "GPS Navigation", "platform": "iOS / Android", "explanation": "Crucial for navigating interior village roads in South Goa where mobile coverage may dip intermittently.", "app_link": "", "recommended": True}
        ],
        "culture_guides": [
            {"category": "DO", "title": "Respect Religious Sites & Churches", "description": "Dress modestly covering shoulders and knees when visiting Old Goa churches and ancient temples.", "importance_level": "Crucial"},
            {"category": "DONT", "title": "Do Not Walk in Swimwear in Town Centres", "description": "Beachwear and bikinis are standard on sandy shores, but wear shorts and shirts when walking into town or dining at town eateries.", "importance_level": "High"},
            {"category": "Dining Etiquette", "title": "Susegad Lifestyle & Afternoon Siesta", "description": "Smaller heritage stores and local family-run taverns frequently observe quiet afternoon hours between 1:30 PM to 4:00 PM.", "importance_level": "Standard"},
            {"category": "Useful Phrases", "title": "Basic Konkani Greetings", "description": "'Dev borem korum' (May God bless you / Thank you), 'Kitem cholta?' (What's happening / How are you?), 'Haav baro aasa' (I am good).", "importance_level": "Standard"}
        ],
        "safety_info": [
            {"category": "General Safety", "title": "Ocean Swimming & Monsoon Riptides", "description": "Observe red beach flags strictly. Rip currents are dangerous during monsoon months (June-September). Always swim near designated lifeguard towers.", "severity": "Warning"},
            {"category": "Scam Awareness", "title": "Unregistered Water Sports Operators", "description": "Book motorized water sports (jet skis, parasailing) only from Goa Tourism certified counters with valid life vests.", "severity": "Advisory"},
            {"category": "Night Safety", "title": "Well-lit Coastal Roads", "description": "North Goa beaches are lively late into the night, but exercise caution on unlit rural bike routes; avoid riding under intoxication.", "severity": "Notice"}
        ],
        "emergency_contacts": [
            {"service_type": "Police Emergency", "contact_number": "112", "notes": "Unified National Emergency Number"},
            {"service_type": "Ambulance / Medical Emergency", "contact_number": "108", "notes": "Free state ambulance service"},
            {"service_type": "Goa Tourist Police Helpline", "contact_number": "+91 832 2420999", "notes": "Dedicated foreign & domestic tourist assistance"},
            {"service_type": "Fire Service", "contact_number": "101", "notes": "Fire & rescue dispatch"}
        ]
    },
    {
        "name": "Tokyo",
        "country": "Japan",
        "country_code": "JP",
        "currency": "JPY",
        "currency_symbol": "¥",
        "tagline": "Futuristic neon metropolises seamlessly interwoven with timeless Shinto tranquility",
        "description": "Tokyo is the world's most sophisticated urban symphony. From sensory sensory feasts in Shibuya and Akihabara to the serene cedar forests surrounding Meiji Shrine and world-class Michelin gastronomy.",
        "hero_image": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=1600&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=600&q=80",
        "approx_daily_budget": 14000.0,
        "best_time_to_visit": "March to May & September to November",
        "is_featured": True,
        "trending_score": 98,
        "travel_types": ["Solo", "Couple", "Friends", "Family", "Business"],
        "interests": ["Culture", "Food", "Shopping", "Architecture", "Photography", "Hidden Gems"],
        "attractions": [
            {"name": "Senso-ji Temple & Nakamise Street", "category": "Culture", "description": "Tokyo's oldest Buddhist temple founded in 645 AD, entered through the iconic red Kaminarimon Thunder Gate.", "estimated_duration_hours": 2.0, "estimated_cost": 0, "best_time_of_day": "Morning", "location_area": "Asakusa"},
            {"name": "Shibuya Crossing & Hachiko Memorial", "category": "Photography", "description": "The world's busiest pedestrian crossing, pulsating with neon giant screens and synchronized crowds.", "estimated_duration_hours": 1.5, "estimated_cost": 0, "best_time_of_day": "Evening", "location_area": "Shibuya"},
            {"name": "Meiji Jingu Shrine Cedar Forest", "category": "Spiritual", "description": "Tranquil 170-acre forest shrine dedicated to Emperor Meiji, offering an oasis of calm right next to Harajuku.", "estimated_duration_hours": 2.0, "estimated_cost": 0, "best_time_of_day": "Morning", "location_area": "Harajuku"},
            {"name": "TeamLab Planets Immersive Digital Art", "category": "Adventure", "description": "Body-immersive digital museum where visitors walk barefoot through water filled with floating light koi fish.", "estimated_duration_hours": 2.5, "estimated_cost": 3800, "best_time_of_day": "Afternoon", "location_area": "Toyosu"},
            {"name": "Tsukiji Outer Market Food Tasting", "category": "Food", "description": "Vibrant street food alleys offering fresh tuna nigiri, tamagoyaki egg omelettes, and grilled wagyu skewers.", "estimated_duration_hours": 2.0, "estimated_cost": 2500, "best_time_of_day": "Morning", "location_area": "Tsukiji"}
        ],
        "local_services": [
            {"category": "Getting Around", "name": "Suica / Pasmo IC Card (Digital Apple/Google Wallet)", "purpose": "Tap-to-ride Subway, Train & Vending payment", "platform": "iOS / Android / Physical Card", "explanation": "Essential transit card for all JR East trains, Tokyo Metro lines, and 7-Eleven convenience payments.", "app_link": "https://www.jreast.co.jp/e/pass/suica.html", "recommended": True},
            {"category": "Getting Around", "name": "GO Taxi (JapanTaxi)", "purpose": "Ride-Hailing", "platform": "iOS / Android", "explanation": "Top taxi-hailing app supporting foreign credit cards with automated Japanese destination translation.", "app_link": "https://go.mo-t.com/en", "recommended": True},
            {"category": "Navigation", "name": "Navitime Japan Travel / Google Maps", "purpose": "Subway Platform & Exit Routing", "platform": "iOS / Android", "explanation": "Detailed step-by-step guidance showing which train car to board for immediate station transfers.", "app_link": "https://japantravel.navitime.com/en/", "recommended": True},
            {"category": "Food Delivery", "name": "Uber Eats Japan / Wolt", "purpose": "Citywide Food Delivery", "platform": "iOS / Android", "explanation": "Supports English language interface and non-Japanese credit cards.", "app_link": "https://ubereats.com", "recommended": True},
            {"category": "Payments", "name": "PayPay / Contactless Credit Cards", "purpose": "QR & NFC Merchant Payments", "platform": "Mobile App", "explanation": "Cash is still respected at traditional food stalls, carry ¥5,000–¥10,000 in notes.", "app_link": "", "recommended": True},
            {"category": "eSIM & SIM", "name": "Airalo / Ubigi Japan eSIM", "purpose": "Instant Local 5G Data", "platform": "eSIM App", "explanation": "Instant digital setup without swapping physical cards. High reliability on NTT Docomo or SoftBank.", "app_link": "https://airalo.com", "recommended": True}
        ],
        "culture_guides": [
            {"category": "DO", "title": "Stand on the Left of Escalators in Tokyo", "description": "Stand quietly on the left side of escalators to let commuters pass on the right (unlike Osaka which is opposite).", "importance_level": "High"},
            {"category": "DONT", "title": "Never Stick Chopsticks Vertically in Rice", "description": "This resembles funerary incense rituals (Tsukitate-bashi) and is strictly considered inauspicious.", "importance_level": "Crucial"},
            {"category": "DONT", "title": "Do Not Walk While Eating on the Street", "description": "Consume street food near the stall where you bought it, or dispose of trash at the stall's bin before moving.", "importance_level": "Standard"},
            {"category": "Tipping", "title": "Zero Tipping Policy", "description": "Tipping is not customary in Japan and can cause confusion or embarrassment. Excellent service is standard.", "importance_level": "Crucial"},
            {"category": "Useful Phrases", "title": "Key Japanese Travel Phrases", "description": "'Arigatou gozaimasu' (Thank you very much), 'Sumimasen' (Excuse me / Sorry), 'Kore wa ikura desu ka?' (How much is this?), 'Eigo ga hanasemasu ka?' (Can you speak English?).", "importance_level": "Standard"}
        ],
        "safety_info": [
            {"category": "General Safety", "title": "One of the World's Safest Megacities", "description": "Tokyo ranks among the safest destinations worldwide. Lost wallets are routinely handed to police koban boxes.", "severity": "Notice"},
            {"category": "Scam Awareness", "title": "Kabukicho Bar & Club Touts", "description": "Never follow touts on the street in nightlife districts (Roppongi/Kabukicho) promising 'cheap drinks' or no cover charge.", "severity": "Warning"},
            {"category": "Natural Safety", "title": "Earthquake Readiness", "description": "Download the 'Safety Tips' app by Japan Tourism Agency for real-time multilingual earthquake/tsunami advisories.", "severity": "Advisory"}
        ],
        "emergency_contacts": [
            {"service_type": "Police Emergency", "contact_number": "110", "notes": "Police dispatch (English translators available on line)"},
            {"service_type": "Ambulance / Fire", "contact_number": "119", "notes": "Fire & medical emergency"},
            {"service_type": "Japan National Tourism Organization (JNTO) Helpline", "contact_number": "050-3816-2720", "notes": "24/7 tourist multilingual assistance (English, Chinese, Korean)"},
            {"service_type": "Metropolitan Police General Counseling", "contact_number": "#9110", "notes": "Non-emergency police inquiries"}
        ]
    },
    {
        "name": "Dubai",
        "country": "United Arab Emirates",
        "country_code": "AE",
        "currency": "AED",
        "currency_symbol": "AED",
        "tagline": "World-class architectural marvels, Arabian desert safaris, and luxury glamour",
        "description": "Dubai is a futuristic desert jewel celebrated for sky-piercing towers, colossal shopping experiences, desert dune sunsets, and multicultural global gastronomy.",
        "hero_image": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=1600&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=600&q=80",
        "approx_daily_budget": 500.0,
        "best_time_to_visit": "November to March",
        "is_featured": True,
        "trending_score": 93,
        "travel_types": ["Family", "Couple", "Luxury", "Business", "Friends"],
        "interests": ["Luxury", "Shopping", "Architecture", "Adventure", "Food", "Beaches"],
        "attractions": [
            {"name": "Burj Khalifa At The Top", "category": "Architecture", "description": "Observation deck on the 124th & 125th floors of the world's tallest skyscraper.", "estimated_duration_hours": 2.0, "estimated_cost": 179, "best_time_of_day": "Late Afternoon", "location_area": "Downtown Dubai"},
            {"name": "Desert Safari with Dune Bashing & BBQ", "category": "Adventure", "description": "4x4 sand dune cruising, camel rides, sandboarding, and stargazing dinner in the Arabian dunes.", "estimated_duration_hours": 6.0, "estimated_cost": 220, "best_time_of_day": "Afternoon", "location_area": "Dubai Desert"},
            {"name": "Museum of the Future", "category": "Architecture", "description": "Architectural wonder adorned with Arabic calligraphy poetry, showcasing 50-year technological horizons.", "estimated_duration_hours": 2.5, "estimated_cost": 149, "best_time_of_day": "Morning", "location_area": "Sheikh Zayed Road"},
            {"name": "Dubai Marina Yacht Cruise", "category": "Luxury", "description": "Glide along skyscrapers and artificial canal islands with panoramic views of Ain Dubai.", "estimated_duration_hours": 2.0, "estimated_cost": 180, "best_time_of_day": "Sunset", "location_area": "Dubai Marina"}
        ],
        "local_services": [
            {"category": "Getting Around", "name": "Careem / Uber", "purpose": "Super-App Ride Hailing & Hala Taxis", "platform": "iOS / Android", "explanation": "Careem enables booking affordable city Hala Taxis and premium limousines with upfront fares.", "app_link": "https://careem.com", "recommended": True},
            {"category": "Getting Around", "name": "Nol Card (Dubai Metro & Tram)", "purpose": "Driverless Metro Transit", "platform": "Physical Card", "explanation": "Red/Silver card for Dubai's pristine driverless metro network connecting DXB Airport to Downtown.", "app_link": "", "recommended": True},
            {"category": "Food Delivery", "name": "Talabat / Deliveroo", "purpose": "Citywide Food Delivery", "platform": "iOS / Android", "explanation": "Super-fast deliveries covering gourmet dining, shawarmas, and groceries.", "app_link": "https://talabat.com", "recommended": True},
            {"category": "Payments", "name": "Apple Pay / Google Pay / Cards", "purpose": "Contactless Payments", "platform": "NFC", "explanation": "Almost completely cashless city. Even small corner stores accept contactless cards.", "app_link": "", "recommended": True},
            {"category": "eSIM & SIM", "name": "Du / Etisalat (e&)", "purpose": "Tourist Mobile SIM", "platform": "Airport Immigrations", "explanation": "Free complimentary tourist SIM with 1GB data is often handed out at DXB immigration.", "app_link": "", "recommended": True}
        ],
        "culture_guides": [
            {"category": "DO", "title": "Dress Respectfully in Public Malls & Old Quarters", "description": "Ensure shoulders and knees are covered when visiting traditional souks, administrative buildings, and family malls.", "importance_level": "Crucial"},
            {"category": "DONT", "title": "Avoid Public Displays of Affection (PDA)", "description": "Holding hands is generally tolerated for married couples, but kissing or aggressive affection in public is prohibited.", "importance_level": "Crucial"},
            {"category": "Photography", "title": "Ask Permission Before Photographing Locals", "description": "Strictly refrain from taking photos of Emirati women, government, military, or airport installations.", "importance_level": "Crucial"}
        ],
        "safety_info": [
            {"category": "General Safety", "title": "Strict Law Enforcement & Ultra Safe", "description": "Dubai is consistently ranked in the top 3 safest cities globally for solo and female travellers.", "severity": "Notice"},
            {"category": "Weather Alert", "title": "Summer Desert Heat", "description": "Between June and August temperatures exceed 44°C (111°F). Schedule outdoor activities early morning or after sunset.", "severity": "Warning"}
        ],
        "emergency_contacts": [
            {"service_type": "Police Emergency", "contact_number": "999", "notes": "Dubai Police General Headquarters"},
            {"service_type": "Ambulance", "contact_number": "998", "notes": "Medical emergency dispatch"},
            {"service_type": "Fire Department (Civil Defence)", "contact_number": "997", "notes": "Civil Defence emergency"},
            {"service_type": "Tourist Police Helpline", "contact_number": "901", "notes": "Tourist assistance & inquiries"}
        ]
    },
    {
        "name": "Paris",
        "country": "France",
        "country_code": "FR",
        "currency": "EUR",
        "currency_symbol": "€",
        "tagline": "The City of Light, romantic boulevards, monumental art, and café culture",
        "description": "Paris beckons with iconic silhouettes like the Eiffel Tower, the world's most treasure-filled museums, Haussmannian avenues, and quintessential sidewalk café bistros.",
        "hero_image": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=1600&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=600&q=80",
        "approx_daily_budget": 160.0,
        "best_time_to_visit": "April to June & September to October",
        "is_featured": True,
        "trending_score": 96,
        "travel_types": ["Couple", "Honeymoon", "Solo", "Family", "Friends"],
        "interests": ["Culture", "Architecture", "Food", "History", "Photography", "Luxury"],
        "attractions": [
            {"name": "Eiffel Tower & Champ de Mars", "category": "Architecture", "description": "The timeless iron symbol of Paris with breathtaking views stretching across the Seine river valley.", "estimated_duration_hours": 2.5, "estimated_cost": 29, "best_time_of_day": "Sunset", "location_area": "7th Arrondissement"},
            {"name": "Musée du Louvre", "category": "Culture", "description": "The world's largest art museum, home to Da Vinci's Mona Lisa and the Winged Victory of Samothrace.", "estimated_duration_hours": 3.5, "estimated_cost": 22, "best_time_of_day": "Morning", "location_area": "1st Arrondissement"},
            {"name": "Montmartre & Sacré-Cœur Basilica", "category": "Viewpoint", "description": "Bohemian hilltop quarter featuring cobblestone alleys, street painters, and panoramic skyline vistas.", "estimated_duration_hours": 2.5, "estimated_cost": 0, "best_time_of_day": "Afternoon", "location_area": "18th Arrondissement"},
            {"name": "Seine River Sunset Cruise", "category": "Relaxation", "description": "Gliding under historic stone bridges past illuminated monuments and Notre-Dame cathedral.", "estimated_duration_hours": 1.5, "estimated_cost": 18, "best_time_of_day": "Evening", "location_area": "Pont Neuf"}
        ],
        "local_services": [
            {"category": "Getting Around", "name": "Bonjour RATP / Citymapper", "purpose": "Metro & Bus Realtime Navigation", "platform": "iOS / Android", "explanation": "Indispensable navigation tools for the dense Paris Métro, RER, and bus system.", "app_link": "https://bonjour-ratp.fr", "recommended": True},
            {"category": "Getting Around", "name": "Bolt / Uber / G7 Taxi", "purpose": "Ride-Hailing & Official Taxi", "platform": "iOS / Android", "explanation": "G7 is Paris's official taxi fleet with bus-lane privileges avoiding heavy Parisian traffic jams.", "app_link": "https://www.g7.fr/en/", "recommended": True},
            {"category": "Food Delivery", "name": "Deliveroo / TheFork (LaFourchette)", "purpose": "Bistro Booking & Dining Discounts", "platform": "iOS / Android", "explanation": "TheFork is widely used for reserving top tables often with 20% to 50% discounts.", "app_link": "https://thefork.com", "recommended": True},
            {"category": "Payments", "name": "Contactless Visa / Mastercard", "purpose": "Everyday Purchases", "platform": "NFC", "explanation": "Contactless payment (Sans contact) is ubiquitous from boulangeries to museums.", "app_link": "", "recommended": True},
            {"category": "eSIM & SIM", "name": "Orange Holiday Europe / Bouygues eSIM", "purpose": "EU-wide Mobile Data", "platform": "eSIM", "explanation": "High-speed 5G connectivity with free EU-wide roaming capabilities.", "app_link": "", "recommended": True}
        ],
        "culture_guides": [
            {"category": "DO", "title": "Always Say 'Bonjour' Before Speaking", "description": "Entering any bakery, shop, or greeting a waiter without saying 'Bonjour Madame/Monsieur' is considered very impolite.", "importance_level": "Crucial"},
            {"category": "Dining Etiquette", "title": "Ask for the Bill ('L'addition s'il vous plaît')", "description": "French waiters will not rush you or bring the bill automatically until you explicitly ask for it.", "importance_level": "Standard"},
            {"category": "DONT", "title": "Do Not Expect Fast Dining", "description": "Meals are an artful leisurely experience. Plan at least 1.5 to 2 hours for dinner in bistros.", "importance_level": "Standard"},
            {"category": "Useful Phrases", "title": "Essential French Courtesies", "description": "'Bonjour' (Good day / Hello), 'S'il vous plaît' (Please), 'Merci beaucoup' (Thank you very much), 'Parlez-vous anglais?' (Do you speak English?).", "importance_level": "High"}
        ],
        "safety_info": [
            {"category": "Scam Awareness", "title": "Pickpocketing & Petition Scams", "description": "Watch your belongings near Eiffel Tower, Louvre, and Gare du Nord. Beware groups asking to sign fake deaf petitions.", "severity": "Warning"},
            {"category": "Scam Awareness", "title": "The Gold Ring & Friendship Bracelet Scams", "description": "Firmly say 'Non merci' and walk away if strangers attempt to tie string bracelets to your wrist at Montmartre.", "severity": "Warning"},
            {"category": "General Safety", "title": "Metro Late Night Awareness", "description": "Keep phones and wallets inside zipped front pockets while riding lines 1, 2, and 4 during crowded rush hours.", "severity": "Notice"}
        ],
        "emergency_contacts": [
            {"service_type": "European Unified Emergency", "contact_number": "112", "notes": "Multilingual EU emergency operator"},
            {"service_type": "SAMU (Medical Emergency / Ambulance)", "contact_number": "15", "notes": "Direct French emergency medical dispatch"},
            {"service_type": "Police Secours", "contact_number": "17", "notes": "National police response"},
            {"service_type": "Fire Brigade (Pompiers)", "contact_number": "18", "notes": "Pompiers de Paris (handles trauma & fires)"}
        ]
    },
    {
        "name": "Singapore",
        "country": "Singapore",
        "country_code": "SG",
        "currency": "SGD",
        "currency_symbol": "S$",
        "tagline": "A clean, green garden city pulsating with futuristic architecture and hawker street feasts",
        "description": "Singapore is an ultra-modern city-state renowned for Gardens by the Bay, UNESCO-recognized hawker food centres, verdant rain trees, and seamless public infrastructure.",
        "hero_image": "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?auto=format&fit=crop&w=1600&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?auto=format&fit=crop&w=600&q=80",
        "approx_daily_budget": 180.0,
        "best_time_to_visit": "All year round (Tropical climate)",
        "is_featured": True,
        "trending_score": 92,
        "travel_types": ["Family", "Couple", "Solo", "Friends", "Business"],
        "interests": ["Nature", "Food", "Architecture", "Shopping", "Luxury", "Photography"],
        "attractions": [
            {"name": "Gardens by the Bay & Supertree Grove", "category": "Nature", "description": "Futuristic vertical botanical gardens featuring high-tech biodomes and nightly light-and-sound shows.", "estimated_duration_hours": 3.0, "estimated_cost": 28, "best_time_of_day": "Evening", "location_area": "Marina Bay"},
            {"name": "Marina Bay Sands SkyPark Observation Deck", "category": "Viewpoint", "description": "Iconic cantilevered observation deck offering 360-degree vistas across Singapore Strait and city skyline.", "estimated_duration_hours": 1.5, "estimated_cost": 32, "best_time_of_day": "Sunset", "location_area": "Marina Bay"},
            {"name": "Maxwell Hawker Centre Feast", "category": "Food", "description": "Sample UNESCO-inscribed hawker delicacies like Tian Tian Hainanese Chicken Rice and laksa noodles.", "estimated_duration_hours": 1.5, "estimated_cost": 8, "best_time_of_day": "Afternoon", "location_area": "Chinatown"},
            {"name": "Sentosa Island & Palawan Beach", "category": "Beaches", "description": "Tropical resort island with sandy beaches, beach clubs, and theme parks connected by cable car.", "estimated_duration_hours": 4.0, "estimated_cost": 15, "best_time_of_day": "Morning", "location_area": "Sentosa"}
        ],
        "local_services": [
            {"category": "Getting Around", "name": "Grab / Gojek", "purpose": "Southeast Asia's Primary Ride App", "platform": "iOS / Android", "explanation": "Primary ride-hailing and food delivery platform across Singapore with transparent fixed pricing.", "app_link": "https://grab.com", "recommended": True},
            {"category": "Getting Around", "name": "SimplyGo (Direct Credit Card Contactless)", "purpose": "Tap-and-Go MRT & Bus", "platform": "NFC Credit Card / Phone", "explanation": "No ticket purchase needed! Tap your international Visa/Mastercard or phone directly on train turnstiles.", "app_link": "https://simplygo.com.sg", "recommended": True},
            {"category": "Food Delivery", "name": "GrabFood / Foodpanda", "purpose": "Local Cuisine Delivery", "platform": "iOS / Android", "explanation": "Order from hawkers and restaurants directly to your hotel lobby.", "app_link": "", "recommended": True},
            {"category": "Payments", "name": "PayNow / NETS / Credit Cards", "purpose": "Cashless Society", "platform": "Mobile App / Card", "explanation": "Even hawker stalls accept contactless card or QR payments.", "app_link": "", "recommended": True},
            {"category": "eSIM & SIM", "name": "Singtel / StarHub Tourist eSIM", "purpose": "100GB 5G High-Speed Data", "platform": "eSIM", "explanation": "Affordable 100GB tourist plans available instantly before departure.", "app_link": "", "recommended": True}
        ],
        "culture_guides": [
            {"category": "DO", "title": "Reserve Hawker Tables with Tissue Packets ('Choping')", "description": "Placing a pocket packet of tissues or an umbrella on a table is the local way of reserving a seat while you order food.", "importance_level": "Standard"},
            {"category": "DONT", "title": "Strict Chewing Gum & Littering Laws", "description": "Importing or selling chewing gum is banned. Heavy fines apply for littering, jaywalking, or smoking in unauthorized zones.", "importance_level": "Crucial"},
            {"category": "DO", "title": "Return Your Food Tray at Hawker Centres", "description": "Under Singapore law, dining patrons must clear their trays and crockeries to designated tray return stations.", "importance_level": "High"},
            {"category": "Useful Phrases", "title": "Singlish Basics", "description": "'Can / Cannot' (Yes that's fine / No that's not possible), 'Shiok!' (Extremely delicious / fantastic!), 'Chio' (Beautiful).", "importance_level": "Standard"}
        ],
        "safety_info": [
            {"category": "General Safety", "title": "Consistently Ranked Safest City Globally", "description": "Low crime rates, clean streets, and high public vigilance make it exceptionally safe 24/7.", "severity": "Notice"},
            {"category": "Health & Weather", "title": "Hydration in Tropical Humidity", "description": "High humidity and equatorial sunshine require drinking abundant water. Tap water in Singapore is completely safe to drink.", "severity": "Notice"}
        ],
        "emergency_contacts": [
            {"service_type": "Police Emergency", "contact_number": "999", "notes": "Singapore Police Force"},
            {"service_type": "Civil Defence Emergency Ambulance / Fire", "contact_number": "995", "notes": "Emergency ambulance dispatch"},
            {"service_type": "Non-Emergency Ambulance", "contact_number": "1777", "notes": "For non-critical transfers"},
            {"service_type": "Tourist Information Hotline", "contact_number": "1800 736 2000", "notes": "Singapore Tourism Board helpline"}
        ]
    },
    {
        "name": "Jaipur",
        "country": "India",
        "country_code": "IN",
        "currency": "INR",
        "currency_symbol": "₹",
        "tagline": "The Pink City of regal forts, hand-block prints, and royal Rajasthani palaces",
        "description": "Capital of Rajasthan, Jaipur boasts terracotta-pink walled cities, hill-cresting Amber fortresses, astrological observatories, and vibrant jewel bazaars.",
        "hero_image": "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=1600&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=600&q=80",
        "approx_daily_budget": 3000.0,
        "best_time_to_visit": "October to March",
        "is_featured": True,
        "trending_score": 90,
        "travel_types": ["Family", "Couple", "Honeymoon", "Solo", "Group Tour"],
        "interests": ["History", "Architecture", "Culture", "Shopping", "Photography", "Food"],
        "attractions": [
            {"name": "Amber Fort & Palace", "category": "History", "description": "Majestic hilltop fort with Sheesh Mahal (Mirror Palace) overlooking Maota Lake.", "estimated_duration_hours": 3.0, "estimated_cost": 500, "best_time_of_day": "Morning", "location_area": "Amer"},
            {"name": "Hawa Mahal (Palace of Winds)", "category": "Architecture", "description": "Five-story pink sandstone honeycomb facade with 953 intricately carved jharokhas.", "estimated_duration_hours": 1.5, "estimated_cost": 200, "best_time_of_day": "Morning", "location_area": "Walled City"},
            {"name": "City Palace & Museum", "category": "Culture", "description": "Royal residence featuring courtyards, textiles, armory, and the famous peacock doorway.", "estimated_duration_hours": 2.5, "estimated_cost": 700, "best_time_of_day": "Afternoon", "location_area": "Old City"},
            {"name": "Nahargarh Fort Sunset Point", "category": "Viewpoint", "description": "Perched on the edge of the Aravalli hills with sweeping panoramic views of Jaipur glowing at dusk.", "estimated_duration_hours": 2.0, "estimated_cost": 200, "best_time_of_day": "Sunset", "location_area": "Nahargarh"}
        ],
        "local_services": [
            {"category": "Getting Around", "name": "Uber / Ola Cabs", "purpose": "App Taxi & Auto Booking", "platform": "iOS / Android", "explanation": "Reliable for rides to Amber Fort and airport with predetermined pricing.", "app_link": "https://uber.com", "recommended": True},
            {"category": "Getting Around", "name": "Jaipur Metro", "purpose": "Clean City Transit", "platform": "Metro Token / Card", "explanation": "Quick connection between Mansarovar and Chandpole / Badi Chaupar (Hawa Mahal).", "app_link": "", "recommended": True},
            {"category": "Food Delivery", "name": "Zomato / Swiggy", "purpose": "Authentic Rajasthani Thali Delivery", "platform": "iOS / Android", "explanation": "Order Dal Baati Churma, Pyaaz Kachori, and sweets from Rawat Mishtan Bhandar.", "app_link": "https://zomato.com", "recommended": True},
            {"category": "Payments", "name": "UPI (Google Pay, PhonePe)", "purpose": "Instant QR Payments", "platform": "iOS / Android", "explanation": "Accepted by gemstone jewelers, handicraft emporiums, and tea stalls alike.", "app_link": "", "recommended": True},
            {"category": "eSIM & SIM", "name": "Airtel / Jio SIM", "purpose": "Local Connectivity", "platform": "City Retail Outlets", "explanation": "Fast 4G/5G coverage throughout the city and heritage monuments.", "app_link": "", "recommended": True}
        ],
        "culture_guides": [
            {"category": "DO", "title": "Bargain Politely in Heritage Bazaars", "description": "Friendly haggling is customary at Johari and Bapu Bazaars. Always remain courteous and smiling.", "importance_level": "Standard"},
            {"category": "DO", "title": "Respect Royal Premises & Courtyards", "description": "Certain sections of the City Palace remain the private residence of the Jaipur royal family; heed signage.", "importance_level": "High"},
            {"category": "Useful Phrases", "title": "Hindi & Rajasthani Greetings", "description": "'Namaste' / 'Khamma Ghani' (Warm traditional Rajasthani greeting), 'Dhanyavaad' (Thank you), 'Kitne ka hai?' (How much is this?).", "importance_level": "Standard"}
        ],
        "safety_info": [
            {"category": "Scam Awareness", "title": "Gemstone & Carpet Commission Guides", "description": "Some unlicensed auto drivers offer to take you to 'government certified' gem or carpet factories for commissions. Firmly decline.", "severity": "Warning"},
            {"category": "General Safety", "title": "Summer Desert Temperatures", "description": "Jaipur temperatures can exceed 42°C in May-June. Visit open-air forts before 11:00 AM or after 4:00 PM.", "severity": "Advisory"}
        ],
        "emergency_contacts": [
            {"service_type": "Unified Emergency Response", "contact_number": "112", "notes": "National Emergency Service"},
            {"service_type": "Ambulance", "contact_number": "108", "notes": "Free state ambulance service"},
            {"service_type": "Rajasthan Tourist Police", "contact_number": "+91 141 2227442", "notes": "Dedicated assistance at major monuments"}
        ]
    },
    {
        "name": "Rome",
        "country": "Italy",
        "country_code": "IT",
        "currency": "EUR",
        "currency_symbol": "€",
        "tagline": "The Eternal City of gladiatorial amphitheaters, baroque fountains, and legendary pasta",
        "description": "Rome is an open-air museum where ancient Colosseum arches stand beside bustling espresso bars, Renaissance piazzas, and Vatican masterpieces.",
        "hero_image": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?auto=format&fit=crop&w=1600&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?auto=format&fit=crop&w=600&q=80",
        "approx_daily_budget": 140.0,
        "best_time_to_visit": "April to May & September to October",
        "is_featured": True,
        "trending_score": 96,
        "travel_types": ["Couple", "History", "Family", "Solo", "Honeymoon"],
        "interests": ["History", "Architecture", "Food", "Culture", "Photography"],
        "attractions": [
            {"name": "Colosseum & Roman Forum", "category": "History", "description": "Iconic Flavian amphitheatre and ancient epicentre of Roman political civic life.", "estimated_duration_hours": 3.0, "estimated_cost": 18, "best_time_of_day": "Morning", "location_area": "Piazza del Colosseo"},
            {"name": "Trevi Fountain Coin Toss", "category": "Architecture", "description": "Breathtaking late-Baroque fountain designed by Nicola Salvi where tossing a coin guarantees a return to Rome.", "estimated_duration_hours": 1.0, "estimated_cost": 0, "best_time_of_day": "Evening", "location_area": "Trevi"},
            {"name": "Vatican Museums & Sistine Chapel", "category": "Culture", "description": "Marvel at Michelangelo's ceiling frescoes and centuries of papal classical sculpture collections.", "estimated_duration_hours": 3.5, "estimated_cost": 25, "best_time_of_day": "Morning", "location_area": "Vatican City"},
            {"name": "Trastevere Cobblestone Culinary Walk", "category": "Food", "description": "Wander bohemian ivy-draped alleys tasting authentic Cacio e Pepe and artisan gelato.", "estimated_duration_hours": 2.5, "estimated_cost": 20, "best_time_of_day": "Evening", "location_area": "Trastevere"}
        ],
        "local_services": [
            {"category": "Getting Around", "name": "FreeNow / Taxi / Metro ATAC", "purpose": "Rome Transit & Cabs", "platform": "iOS / Android", "explanation": "ATAC Metro lines A and B connect Termini station to Colosseum and Vatican.", "app_link": "https://www.atac.roma.it", "recommended": True},
            {"category": "Food Delivery", "name": "Glovo / Deliveroo Italy", "purpose": "Italian Trattoria & Pizza Delivery", "platform": "iOS / Android", "explanation": "Convenient for having Roman pinsa and wood-fired pizza delivered to your accommodation.", "app_link": "https://glovoapp.com", "recommended": True},
            {"category": "Payments", "name": "Contactless Visa / Mastercard", "purpose": "Cards & Apple Pay", "platform": "NFC", "explanation": "Widely accepted; carry €10-€20 cash for small espresso bars (banco).", "app_link": "", "recommended": True},
            {"category": "eSIM & SIM", "name": "TIM / Vodafone Italy eSIM", "purpose": "Fast Local 5G Data", "platform": "eSIM", "explanation": "High coverage across Lazio region and historic cobblestone center.", "app_link": "", "recommended": True}
        ],
        "culture_guides": [
            {"category": "DO", "title": "Drink Espresso Standing at the Counter (Banco)", "description": "Drinking coffee standing at the bar counter is customary and costs significantly less than sitting at outside tables.", "importance_level": "Standard"},
            {"category": "DONT", "title": "No Cappuccino After 11:00 AM", "description": "Italians consider milk-heavy coffee strictly for morning digestion; ordering cappuccino after lunch or dinner is seen as unusual.", "importance_level": "Standard"},
            {"category": "Dress", "title": "Cover Shoulders and Knees in Basilicas", "description": "Strict dress codes are enforced at St. Peter's Basilica, Pantheon, and churches across Rome.", "importance_level": "Crucial"},
            {"category": "Useful Phrases", "title": "Italian Essentials", "description": "'Buongiorno' (Good morning), 'Grazie mille' (Thank you so much), 'Per favore' (Please), 'Quanto costa?' (How much is this?).", "importance_level": "High"}
        ],
        "safety_info": [
            {"category": "Scam Awareness", "title": "Pickpocketing on Metro Line A & Termini", "description": "Stay alert during crowded transit stops at Termini and Colosseo. Keep bags zipped and in front of you.", "severity": "Warning"},
            {"category": "Scam Awareness", "title": "Gladiator Costumed Photographers", "description": "Men dressed as Roman centurions outside the Colosseum will aggressively demand €20-€50 after posing for a photo. Politely bypass them.", "severity": "Warning"}
        ],
        "emergency_contacts": [
            {"service_type": "European Universal Emergency", "contact_number": "112", "notes": "Carabinieri & State Police operator"},
            {"service_type": "Ambulance (Emergenza Sanitaria)", "contact_number": "118", "notes": "Medical emergency dispatch"},
            {"service_type": "Fire Brigade (Vigili del Fuoco)", "contact_number": "115", "notes": "Fire & emergency rescue"}
        ]
    },
    {
        "name": "London",
        "country": "United Kingdom",
        "country_code": "GB",
        "currency": "GBP",
        "currency_symbol": "£",
        "tagline": "Royal pageantry, world-class West End theatre, and timeless Thames bridges",
        "description": "London pairs imperial British history with global cultural energy: from the Tower of London and Big Ben to vibrant Borough Market culinary stalls and Hyde Park greenery.",
        "hero_image": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=1600&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=600&q=80",
        "approx_daily_budget": 150.0,
        "best_time_to_visit": "May to September",
        "is_featured": True,
        "trending_score": 97,
        "travel_types": ["Solo", "Friends", "Family", "Couple", "Business"],
        "interests": ["History", "Culture", "Architecture", "Food", "Shopping", "Photography"],
        "attractions": [
            {"name": "Tower of London & Crown Jewels", "category": "History", "description": "Nearly 1,000-year-old royal fortress housing the dazzling Crown Jewels and guarded by Yeoman Warders.", "estimated_duration_hours": 3.0, "estimated_cost": 34, "best_time_of_day": "Morning", "location_area": "Tower Hill"},
            {"name": "British Museum", "category": "Culture", "description": "Vast world-renowned collection spanning two million years of human history including the Rosetta Stone (Free admission).", "estimated_duration_hours": 3.5, "estimated_cost": 0, "best_time_of_day": "Afternoon", "location_area": "Bloomsbury"},
            {"name": "Westminster Abbey & Big Ben", "category": "Architecture", "description": "Royal coronation church adjacent to the Houses of Parliament and iconic Elizabeth Tower clock.", "estimated_duration_hours": 2.0, "estimated_cost": 29, "best_time_of_day": "Morning", "location_area": "Westminster"},
            {"name": "Borough Market Street Gastronomy", "category": "Food", "description": "Historic covered market bursting with artisan cheeses, hot salt beef bagels, and gourmet chocolate strawberries.", "estimated_duration_hours": 2.0, "estimated_cost": 15, "best_time_of_day": "Lunch", "location_area": "Southwark"}
        ],
        "local_services": [
            {"category": "Getting Around", "name": "TfL Contactless / Citymapper", "purpose": "Tube, Bus & Overground", "platform": "iOS / Android / Contactless", "explanation": "No Oyster card required! Tap your contactless bank card or phone on yellow readers across the London Underground.", "app_link": "https://tfl.gov.uk", "recommended": True},
            {"category": "Getting Around", "name": "Uber / Bolt / Black Cabs (Gett)", "purpose": "Ride-Hailing & Black Cabs", "platform": "iOS / Android", "explanation": "Traditional black cabs accept card and navigate London's legendary 'Knowledge' geography.", "app_link": "", "recommended": True},
            {"category": "Food Delivery", "name": "Deliveroo / Just Eat", "purpose": "London Restaurant Delivery", "platform": "iOS / Android", "explanation": "Extensive selection from high-end Mayfair dining to East London curry houses.", "app_link": "https://deliveroo.co.uk", "recommended": True},
            {"category": "Payments", "name": "Contactless Visa / Mastercard", "purpose": "Virtually 100% Cashless", "platform": "NFC", "explanation": "London is almost entirely cashless. Even street buskers accept contactless taps.", "app_link": "", "recommended": True},
            {"category": "eSIM & SIM", "name": "EE / Vodafone / Three UK eSIM", "purpose": "UK High-Speed 5G", "platform": "eSIM", "explanation": "Quick activation with strong cellular reception throughout the London Underground 4G network.", "app_link": "", "recommended": True}
        ],
        "culture_guides": [
            {"category": "DO", "title": "Stand on the Right of Escalators", "description": "Strict London etiquette: always stand on the right side of escalators on the Tube to let hurried commuters pass on the left.", "importance_level": "Crucial"},
            {"category": "DO", "title": "Mind the Gap", "description": "Watch the platform gap between the train and platform edge at historic curved Tube stations.", "importance_level": "Standard"},
            {"category": "Etiquette", "title": "Queueing Etiquette", "description": "Never jump or cut a queue at bus stops, ticket desks, or coffee shops; orderly queueing is sacred in British culture.", "importance_level": "Crucial"},
            {"category": "Useful Phrases", "title": "British Slang & Courtesies", "description": "'Cheers' (Thank you / Goodbye), 'Mind the gap' (Watch your footing), 'You alright?' (Standard informal greeting: 'How are you?').", "importance_level": "Standard"}
        ],
        "safety_info": [
            {"category": "Scam Awareness", "title": "Phone Snatching by E-Bike Riders", "description": "Be vigilant when using your phone near the curb in Oxford Circus, Soho, or Westminster; avoid holding phones loosely near roadways.", "severity": "Warning"},
            {"category": "Scam Awareness", "title": "Westminster Bridge Shell Games", "description": "Never participate in three-card monte or cup-and-ball gambling tricks on bridges; they are coordinated scam rings with fake crowd shills.", "severity": "Warning"}
        ],
        "emergency_contacts": [
            {"service_type": "Unified UK Emergency Number", "contact_number": "999", "notes": "Police, Fire, Ambulance & Coastguard"},
            {"service_type": "Non-Emergency Police", "contact_number": "101", "notes": "For reporting non-urgent crimes"},
            {"service_type": "NHS Non-Emergency Health Advice", "contact_number": "111", "notes": "24/7 medical guidance and clinic appointments"}
        ]
    },
    {
        "name": "Bangkok",
        "country": "Thailand",
        "country_code": "TH",
        "currency": "THB",
        "currency_symbol": "฿",
        "tagline": "Golden Buddhist spires, bustling river canals, and the world's most vibrant street food markets",
        "description": "Bangkok is a thrilling contrast of serene glittering wats (temples), high-energy tuk-tuks, luxury riverside hotels, and Michelin-starred street stalls.",
        "hero_image": "https://images.unsplash.com/photo-1508009603885-50cf7c579365?auto=format&fit=crop&w=1600&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1508009603885-50cf7c579365?auto=format&fit=crop&w=600&q=80",
        "approx_daily_budget": 1800.0,
        "best_time_to_visit": "November to February",
        "is_featured": True,
        "trending_score": 94,
        "travel_types": ["Solo", "Friends", "Couple", "Group Tour", "Family"],
        "interests": ["Food", "Culture", "Nightlife", "Shopping", "Spiritual", "Hidden Gems"],
        "attractions": [
            {"name": "The Grand Palace & Wat Phra Kaew", "category": "Culture", "description": "Splendid royal compound housing the sacred Emerald Buddha carved from a single jade block.", "estimated_duration_hours": 3.0, "estimated_cost": 500, "best_time_of_day": "Morning", "location_area": "Phra Nakhon"},
            {"name": "Wat Arun (Temple of Dawn)", "category": "Spiritual", "description": "Majestic riverside Khmer-style prang tower encrusted with colourful porcelain overlooking the Chao Phraya River.", "estimated_duration_hours": 2.0, "estimated_cost": 100, "best_time_of_day": "Late Afternoon", "location_area": "Bangkok Yai"},
            {"name": "Chao Phraya Express River Cruise", "category": "Relaxation", "description": "Glide down Bangkok's historic waterway past ancient temples, stilt houses, and modern skylines.", "estimated_duration_hours": 1.5, "estimated_cost": 30, "best_time_of_day": "Sunset", "location_area": "Sathorn Pier"},
            {"name": "Chatuchak Weekend Market", "category": "Shopping", "description": "Over 15,000 stalls selling vintage clothing, handcrafted ceramics, Thai silk, and street food delicacies.", "estimated_duration_hours": 3.5, "estimated_cost": 0, "best_time_of_day": "Morning", "location_area": "Chatuchak"}
        ],
        "local_services": [
            {"category": "Getting Around", "name": "Grab / Bolt / BTS Skytrain & MRT", "purpose": "Air-Conditioned Urban Transit", "platform": "iOS / Android / BTS Rabbit Card", "explanation": "Use BTS Skytrain to skip heavy street traffic jams. Grab and Bolt provide hassle-free fixed-fare rides.", "app_link": "https://grab.com", "recommended": True},
            {"category": "Food Delivery", "name": "GrabFood / Foodpanda Thailand", "purpose": "Street Food & Thai Restaurant Delivery", "platform": "iOS / Android", "explanation": "Order authentic Pad Thai, Som Tum, and Mango Sticky Rice delivered right to your hotel.", "app_link": "", "recommended": True},
            {"category": "Payments", "name": "PromptPay QR / Cash (Thai Baht)", "purpose": "Everyday Purchases", "platform": "Cash & QR", "explanation": "Carry cash (฿100 and ฿500 notes) for street food stalls and river boats.", "app_link": "", "recommended": True},
            {"category": "eSIM & SIM", "name": "AIS / TrueMove H Tourist eSIM", "purpose": "Fast 5G Connectivity", "platform": "eSIM", "explanation": "Available instantly with unlimited data packages for travellers across Thailand.", "app_link": "", "recommended": True}
        ],
        "culture_guides": [
            {"category": "DO", "title": "The Traditional 'Wai' Greeting", "description": "Slight bow with palms pressed together like a prayer at chest height shows warmth and respect.", "importance_level": "Standard"},
            {"category": "DONT", "title": "Never Touch Anyone's Head or Point Feet", "description": "In Buddhist culture, the head is sacred and the feet are spiritually lowest. Never point soles of your feet at Buddha images or monks.", "importance_level": "Crucial"},
            {"category": "Religion", "title": "Dress Respectfully for Temples", "description": "Cover shoulders, knees, and remove footwear before entering any temple hall (viharn).", "importance_level": "Crucial"},
            {"category": "Useful Phrases", "title": "Thai Courtesies", "description": "'Sawatdee khrap/kha' (Hello), 'Khop khun khrap/kha' (Thank you), 'Tao rai?' (How much?).", "importance_level": "Standard"}
        ],
        "safety_info": [
            {"category": "Scam Awareness", "title": "'The Palace is Closed Today' Tuk-Tuk Scam", "description": "Friendly strangers outside Grand Palace claiming it is closed for royal rituals will offer to take you to gem shops. Ignore them; check official ticket booths yourself.", "severity": "Warning"},
            {"category": "Getting Around", "title": "Always Request Taxi Meter", "description": "When hailing pink/yellow city taxis, firmly insist: 'Meter please' (Mee-ter khrap). If refused, wave for another taxi.", "severity": "Notice"}
        ],
        "emergency_contacts": [
            {"service_type": "Tourist Police (English Speaking)", "contact_number": "1155", "notes": "Dedicated 24/7 tourist assistance hotline"},
            {"service_type": "General Police Emergency", "contact_number": "191", "notes": "Royal Thai Police dispatch"},
            {"service_type": "Medical Emergency & Ambulance", "contact_number": "1669", "notes": "Public medical emergency service"}
        ]
    },
    {
        "name": "Bali",
        "country": "Indonesia",
        "country_code": "ID",
        "currency": "IDR",
        "currency_symbol": "Rp",
        "tagline": "The Island of the Gods, emerald jungle rice terraces, and mystical sea cliff temples",
        "description": "Bali enchants with cascading rice terraces in Ubud, volcanic sunrise treks, world-class surf breaks in Uluwatu, and rich Balinese Hindu ceremonial spirituality.",
        "hero_image": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=1600&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=600&q=80",
        "approx_daily_budget": 650000.0,
        "best_time_to_visit": "April to October",
        "is_featured": True,
        "trending_score": 95,
        "travel_types": ["Honeymoon", "Couple", "Solo", "Friends", "Adventure"],
        "interests": ["Nature", "Beaches", "Spiritual", "Relaxation", "Adventure", "Culture"],
        "attractions": [
            {"name": "Uluwatu Clifftop Temple & Kecak Dance", "category": "Spiritual", "description": "Perched on a 70-meter dramatic sea cliff with hypnotic sunset Kecak fire dance chorus.", "estimated_duration_hours": 2.5, "estimated_cost": 150000, "best_time_of_day": "Sunset", "location_area": "South Kuta"},
            {"name": "Tegallalang Emerald Rice Terraces", "category": "Nature", "description": "Stunning subak traditional irrigation rice paddies carving cascading green amphitheaters through Ubud valleys.", "estimated_duration_hours": 2.0, "estimated_cost": 25000, "best_time_of_day": "Morning", "location_area": "Ubud"},
            {"name": "Mount Batur Sunrise Trek", "category": "Adventure", "description": "Early morning hike up an active volcano with breakfast cooked over natural volcanic steam vents.", "estimated_duration_hours": 5.0, "estimated_cost": 400000, "best_time_of_day": "Dawn", "location_area": "Kintamani"},
            {"name": "Tanah Lot Sea Temple", "category": "Photography", "description": "Iconic offshore rock temple framed against pounding ocean waves and radiant sunset skies.", "estimated_duration_hours": 2.0, "estimated_cost": 75000, "best_time_of_day": "Sunset", "location_area": "Tabanan"}
        ],
        "local_services": [
            {"category": "Getting Around", "name": "Grab / Gojek", "purpose": "App Scooter & Car Taxis", "platform": "iOS / Android", "explanation": "The ultimate Southeast Asia super-apps for cheap scooter rides (Gojek) and private cars.", "app_link": "https://gojek.com", "recommended": True},
            {"category": "Getting Around", "name": "Private Day Driver Hire", "purpose": "Full-Day Exploration", "platform": "Local Hire Desks", "explanation": "Extremely economical for day tours (approx Rp 600,000 / $40 USD per full 10-hour day).", "app_link": "", "recommended": True},
            {"category": "Food Delivery", "name": "GrabFood / GoFood", "purpose": "Cafe & Nasi Goreng Delivery", "platform": "iOS / Android", "explanation": "Delivers smoothie bowls, fresh coconuts, and traditional warung food directly to your villa.", "app_link": "", "recommended": True},
            {"category": "Payments", "name": "QRIS / Cash (Indonesian Rupiah)", "purpose": "QR & Cash Payments", "platform": "QRIS", "explanation": "Local warungs prefer cash. ATMs inside bank branches (BCA, Mandiri) are recommended.", "app_link": "", "recommended": True},
            {"category": "eSIM & SIM", "name": "Telkomsel Tourist SIM", "purpose": "Indonesia's Top Coverage", "platform": "eSIM / Local Stores", "explanation": "Telkomsel has the strongest coverage across beaches, Ubud hills, and Nusa Penida.", "app_link": "", "recommended": True}
        ],
        "culture_guides": [
            {"category": "DO", "title": "Watch Out for Daily 'Canang Sari' Offerings", "description": "Little woven palm-leaf baskets with colorful flowers and incense sit on sidewalks and doorsteps. Step carefully and avoid stepping on them.", "importance_level": "Crucial"},
            {"category": "DO", "title": "Wear a Sarong in Temples", "description": "Both men and women must wear a sarong and sash (selendang) around the waist when entering any temple complex.", "importance_level": "Crucial"},
            {"category": "Etiquette", "title": "Use Your Right Hand", "description": "Always offer payments or hand items over using your right hand, as the left hand is traditionally considered impolite.", "importance_level": "Standard"},
            {"category": "Useful Phrases", "title": "Indonesian Essentials", "description": "'Terima kasih' (Thank you), 'Sama-sama' (You are welcome), 'Berapa harganya?' (How much does this cost?).", "importance_level": "Standard"}
        ],
        "safety_info": [
            {"category": "Health & Water", "title": "Avoid Tap Water ('Bali Belly')", "description": "Drink only bottled, filtered, or boiled water. Use bottled water to brush teeth and avoid unpeeled fruits from roadside carts.", "severity": "Warning"},
            {"category": "Nature Safety", "title": "Mischievous Temple Monkeys", "description": "Monkeys at Uluwatu and Ubud Sacred Monkey Forest will snatch sunglasses, hats, and smartphones. Keep loose items stowed in backpacks.", "severity": "Notice"},
            {"category": "Ocean Safety", "title": "Strong Beach Undertows", "description": "Swim only between red-and-yellow flags on Kuta, Seminyak, and Canggu beaches; reef breaks generate powerful currents.", "severity": "Warning"}
        ],
        "emergency_contacts": [
            {"service_type": "National Police Emergency", "contact_number": "110", "notes": "Indonesian National Police"},
            {"service_type": "Medical Emergency & Ambulance", "contact_number": "118", "notes": "National Ambulance dispatch"},
            {"service_type": "Bali Tourist Police Helpline", "contact_number": "+62 361 754590", "notes": "Assistance for international travellers in Badung/Kuta"}
        ]
    },
    {
        "name": "Sydney",
        "country": "Australia",
        "country_code": "AU",
        "currency": "AUD",
        "currency_symbol": "A$",
        "tagline": "Sun-drenched harbour splendour, iconic sail architectures, and world-class ocean beaches",
        "description": "Sydney sparkles around the world's most glorious natural harbour, featuring the architectural masterpiece Opera House, the iconic Harbour Bridge, coastal clifftop walks, and golden Bondi sands.",
        "hero_image": "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?auto=format&fit=crop&w=1600&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?auto=format&fit=crop&w=600&q=80",
        "approx_daily_budget": 170.0,
        "best_time_to_visit": "September to November & March to May",
        "is_featured": True,
        "trending_score": 93,
        "travel_types": ["Solo", "Friends", "Family", "Couple", "Adventure"],
        "interests": ["Beaches", "Nature", "Architecture", "Food", "Adventure", "Photography"],
        "attractions": [
            {"name": "Sydney Opera House Tour", "category": "Architecture", "description": "UNESCO-inscribed performing arts centre with celebrated expressionist shell designs jutting into the harbour.", "estimated_duration_hours": 2.0, "estimated_cost": 45, "best_time_of_day": "Morning", "location_area": "Bennelong Point"},
            {"name": "Sydney Harbour Bridge Walk or Climb", "category": "Viewpoint", "description": "Stroll across the pedestrian span or scale the steel arch for 360-degree Pacific panorama vistas.", "estimated_duration_hours": 2.5, "estimated_cost": 0, "best_time_of_day": "Morning", "location_area": "The Rocks"},
            {"name": "Bondi to Coogee Coastal Walk", "category": "Nature", "description": "Scenic 6km clifftop pathway winding past Tamarama, Bronte, and Gordon's Bay with crashing ocean surf.", "estimated_duration_hours": 3.0, "estimated_cost": 0, "best_time_of_day": "Late Afternoon", "location_area": "Eastern Suburbs"},
            {"name": "Manly Ferry Ride from Circular Quay", "category": "Relaxation", "description": "World's most scenic public commuter ferry cruise passing Fort Denison and Sydney Heads.", "estimated_duration_hours": 1.5, "estimated_cost": 10, "best_time_of_day": "Sunset", "location_area": "Circular Quay"}
        ],
        "local_services": [
            {"category": "Getting Around", "name": "Opal / Direct Contactless Card", "purpose": "Trains, Ferries, Light Rail & Buses", "platform": "Contactless Visa/Mastercard", "explanation": "Tap your phone or credit card directly on Opal readers at ferry wharves and train gates with daily fare caps.", "app_link": "https://transportnsw.info", "recommended": True},
            {"category": "Getting Around", "name": "Uber / DiDi Australia", "purpose": "Ride-Hailing", "platform": "iOS / Android", "explanation": "Quick pickups from Sydney Airport and across suburban Sydney hubs.", "app_link": "https://uber.com", "recommended": True},
            {"category": "Food Delivery", "name": "DoorDash / Uber Eats Australia", "purpose": "Sydney Food Delivery", "platform": "iOS / Android", "explanation": "Wide selection spanning artisanal brunch, flat whites, Asian fusion, and sourdough bakeries.", "app_link": "", "recommended": True},
            {"category": "Payments", "name": "Contactless Cards / Apple Pay", "purpose": "Tap-and-Go Payments", "platform": "NFC", "explanation": "Almost completely cashless country. Tap-and-go accepted at coffee kiosks and beach bars.", "app_link": "", "recommended": True},
            {"category": "eSIM & SIM", "name": "Telstra / Optus eSIM", "purpose": "High-Speed 5G Nationwide", "platform": "eSIM", "explanation": "Telstra provides the most extensive network coverage across NSW and outback regions.", "app_link": "", "recommended": True}
        ],
        "culture_guides": [
            {"category": "DO", "title": "Swim Strictly Between the Red and Yellow Flags", "description": "Australian surf beaches have powerful rip currents. Volunteer surf lifesavers patrol and flag safe swimming zones.", "importance_level": "Crucial"},
            {"category": "Tipping", "title": "Tipping is Optional", "description": "Australian hospitality workers receive fair award wages. Tipping 10% for exceptional dining is appreciated but never mandatory.", "importance_level": "Standard"},
            {"category": "Etiquette", "title": "Sun Protection ('Slip, Slop, Slap')", "description": "The Southern Hemisphere UV index is exceptionally intense; wear SPF 50+ sunscreen, hats, and sunglasses even on cloudy days.", "importance_level": "Crucial"},
            {"category": "Useful Phrases", "title": "Aussie Slang Basics", "description": "'G'day' (Hello), 'No worries' (You are welcome / It's fine), 'Brekkie' (Breakfast), 'Arvo' (Afternoon).", "importance_level": "Standard"}
        ],
        "safety_info": [
            {"category": "Ocean Safety", "title": "Rip Currents & Bluebottle Jellyfish", "description": "If caught in a rip, stay calm, float, and raise one arm for help. Never fight the current directly.", "severity": "Warning"},
            {"category": "Sun Protection", "title": "High UV Danger", "description": "UV levels routinely hit extreme 11+ from October to March. Reapply water-resistant sunscreen every two hours.", "severity": "Notice"}
        ],
        "emergency_contacts": [
            {"service_type": "Triple Zero (000) National Emergency", "contact_number": "000", "notes": "Police, Ambulance & Fire Brigade"},
            {"service_type": "State Emergency Service (SES)", "contact_number": "132 500", "notes": "For storm and flood assistance"},
            {"service_type": "Poisons Information Centre", "contact_number": "13 11 26", "notes": "24/7 marine sting and venom helpline"}
        ]
    },
    {
        "name": "Barcelona",
        "country": "Spain",
        "country_code": "ES",
        "currency": "EUR",
        "currency_symbol": "€",
        "tagline": "Gaudí's whimsical modernist dreams, vibrant Mediterranean tapas bars, and Gothic Quarter secrets",
        "description": "Barcelona captivates with the soaring spires of the Sagrada Família, Park Güell mosaics, buzzing sidewalk terraces along Las Ramblas, and golden Barceloneta beachfront.",
        "hero_image": "https://images.unsplash.com/photo-1583422409516-2895a77efded?auto=format&fit=crop&w=1600&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1583422409516-2895a77efded?auto=format&fit=crop&w=600&q=80",
        "approx_daily_budget": 130.0,
        "best_time_to_visit": "May to June & September to October",
        "is_featured": True,
        "trending_score": 96,
        "travel_types": ["Friends", "Couple", "Solo", "Honeymoon", "Family"],
        "interests": ["Architecture", "Food", "Beaches", "Culture", "Nightlife", "Photography"],
        "attractions": [
            {"name": "Basílica de la Sagrada Família", "category": "Architecture", "description": "Antoni Gaudí's magnum opus basilica under construction since 1882, renowned for stained-glass forest canopies.", "estimated_duration_hours": 3.0, "estimated_cost": 26, "best_time_of_day": "Morning", "location_area": "Eixample"},
            {"name": "Park Güell Surreal Mosaic Park", "category": "Photography", "description": "Enchanting garden complex of undulating mosaic benches, stone viaducts, and panoramic city vistas.", "estimated_duration_hours": 2.5, "estimated_cost": 10, "best_time_of_day": "Late Afternoon", "location_area": "Gràcia"},
            {"name": "Gothic Quarter (Barri Gòtic) Walk", "category": "History", "description": "Medieval labyrinth of narrow cobblestone alleyways, secluded plazas, and Roman temple remnants.", "estimated_duration_hours": 2.0, "estimated_cost": 0, "best_time_of_day": "Afternoon", "location_area": "Ciutat Vella"},
            {"name": "Mercat de la Boqueria Tapas Crawl", "category": "Food", "description": "Historic food market bursting with jamón ibérico, fresh Mediterranean oysters, and grilled seafood pintxos.", "estimated_duration_hours": 1.5, "estimated_cost": 15, "best_time_of_day": "Lunch", "location_area": "La Rambla"}
        ],
        "local_services": [
            {"category": "Getting Around", "name": "TMB Metro & Bus / Citymapper", "purpose": "Integrated Transit Network", "platform": "T-Casual Ticket / Card", "explanation": "The T-Casual card offers 10 multimodal trips across Barcelona's efficient metro and bus network.", "app_link": "https://www.tmb.cat", "recommended": True},
            {"category": "Getting Around", "name": "FreeNow / Cabify / Bicing", "purpose": "Taxi & Bike Sharing", "platform": "iOS / Android", "explanation": "Official licensed black-and-yellow city cabs can be hailed instantly via FreeNow.", "app_link": "https://free-now.com", "recommended": True},
            {"category": "Food Delivery", "name": "Glovo / Uber Eats Spain", "purpose": "Catalan Dining & Tapas Delivery", "platform": "iOS / Android", "explanation": "Glovo was born in Barcelona; fast delivery for tapas, paella, and pastries.", "app_link": "https://glovoapp.com", "recommended": True},
            {"category": "Payments", "name": "Contactless Visa / Mastercard", "purpose": "Everyday Purchases", "platform": "NFC", "explanation": "Contactless cards accepted everywhere. Carry small cash (€5-€10) for market stalls.", "app_link": "", "recommended": True},
            {"category": "eSIM & SIM", "name": "Movistar / Vodafone Spain eSIM", "purpose": "EU High-Speed 5G", "platform": "eSIM", "explanation": "Superb 5G speed across Catalonia with free roaming throughout Europe.", "app_link": "", "recommended": True}
        ],
        "culture_guides": [
            {"category": "DO", "title": "Adjust to Spanish Dining Hours", "description": "Lunch is typically 1:30 PM–3:30 PM, and dinner rarely starts before 8:30 PM or 9:00 PM in authentic tapas bars.", "importance_level": "Crucial"},
            {"category": "DONT", "title": "Do Not Order Sangria at Tourist Traps on Las Ramblas", "description": "Locals drink vermut (sweet vermouth) or tinto de verano; avoid overpriced giant sangria pitchers on tourist strips.", "importance_level": "Standard"},
            {"category": "Culture", "title": "Catalan Language & Pride", "description": "Both Catalan and Spanish are co-official languages. Appreciating Catalan culture and greetings is warmly welcomed.", "importance_level": "High"},
            {"category": "Useful Phrases", "title": "Spanish & Catalan Courtesies", "description": "'Hola' (Hello), 'Gracias' / 'Moltes gràcies' (Thank you), 'Por favor' / 'Si us plau' (Please), 'La cuenta, por favor' (The bill, please).", "importance_level": "Standard"}
        ],
        "safety_info": [
            {"category": "Scam Awareness", "title": "Pickpocketing Capital Vigilance", "description": "Las Ramblas, Metro Line 3, and Barceloneta beach are notorious hotspots for distraction pickpockets. Never keep phones in back pockets or leave bags unattended on chairs.", "severity": "Warning"},
            {"category": "Scam Awareness", "title": "Bird Dropping / Spilled Drink Scam", "description": "If someone alerts you that a substance fell on your jacket and offers to clean it, firmly back away and protect your belongings.", "severity": "Warning"}
        ],
        "emergency_contacts": [
            {"service_type": "European Unified Emergency", "contact_number": "112", "notes": "Multilingual emergency dispatcher"},
            {"service_type": "Mossos d'Esquadra (Catalan Police)", "contact_number": "088", "notes": "Regional police force"},
            {"service_type": "Medical Emergency (CatSalut)", "contact_number": "061", "notes": "Health emergencies and ambulance"}
        ]
    }
]

ALL_INTERESTS = [
    ("Adventure", "adventure", "mountain", "Thrilling activities, sports, and outdoor treks"),
    ("Nature", "nature", "trees", "Scenic landscapes, parks, and lush wilderness"),
    ("Beaches", "beaches", "waves", "Coastal relaxation, sea views, and water activities"),
    ("History", "history", "landmark", "Heritage monuments, ancient ruins, and historic sites"),
    ("Culture", "culture", "palette", "Museums, performing arts, folklore, and traditions"),
    ("Food", "food", "utensils", "Local street delicacies, culinary tours, and fine dining"),
    ("Shopping", "shopping", "shopping-bag", "Bazaars, luxury malls, and artisan souvenirs"),
    ("Nightlife", "nightlife", "moon", "Lively clubs, sunset bars, and evening entertainment"),
    ("Photography", "photography", "camera", "Picture-perfect viewpoints, architecture, and vistas"),
    ("Luxury", "luxury", "gem", "High-end resorts, fine dining, and VIP experiences"),
    ("Relaxation", "relaxation", "coffee", "Spas, tranquil walks, and leisurely unwinding"),
    ("Spiritual", "spiritual", "sun", "Temples, shrines, and mindfulness retreats"),
    ("Architecture", "architecture", "building", "Iconic landmarks, skyline design, and historic buildings"),
    ("Wildlife", "wildlife", "paw-print", "Animal safaris, marine life, and conservation sanctuaries"),
    ("Hidden Gems", "hidden-gems", "compass", "Off-the-beaten-path secrets loved by locals"),
    ("Local Experiences", "local-experiences", "users", "Hands-on workshops, village walks, and native culture")
]

ALL_TRAVEL_TYPES = [
    ("Solo", "solo", "Safety, flexible pacing, and authentic personal discovery", "Focused on safety, budget freedom, and immersive solo adventures."),
    ("Friends", "friends", "Nightlife, adventure, sharing, and memorable fun", "Geared for energetic pacing, shared group activities, food, and nightlife."),
    ("Family", "family", "Comfort, kids-friendly spots, and relaxed logistics", "Curated for family safety, comfortable schedules, and all-age attractions."),
    ("Couple", "couple", "Romantic scenic spots, fine meals, and intimacy", "Romantic viewpoints, intimate dinners, and charming wanderings."),
    ("Honeymoon", "honeymoon", "Unforgettable luxury, romance, and pampered tranquility", "Premium stays, serene sunset cruises, and private memorable moments."),
    ("Senior Citizens", "senior-citizens", "Gentle pacing, accessibility, and comfortable transit", "Easy walking routes, elevator-accessible monuments, and restful afternoons."),
    ("Business", "business", "Efficient scheduling, work hubs, and quick highlights", "Streamlined agendas, reliable transport, and high-connectivity hotspots."),
    ("Group Tour", "group-tour", "Organized highlights, group transport, and key sights", "Cost-effective routing, group activities, and iconic landmarks.")
]

def seed_database(db: Session):
    # Check if already seeded
    if db.query(Destination).count() > 0:
        return

    # Seed Interests
    interest_map = {}
    for name, slug, icon, desc in ALL_INTERESTS:
        obj = db.query(Interest).filter(Interest.slug == slug).first()
        if not obj:
            obj = Interest(name=name, slug=slug, icon=icon, description=desc)
            db.add(obj)
            db.flush()
        interest_map[name] = obj

    # Seed Travel Types
    travel_type_map = {}
    for name, slug, tagline, desc in ALL_TRAVEL_TYPES:
        obj = db.query(TravelType).filter(TravelType.slug == slug).first()
        if not obj:
            obj = TravelType(name=name, slug=slug, tagline=tagline, description=desc)
            db.add(obj)
            db.flush()
        travel_type_map[name] = obj

    # Seed Countries & Destinations
    for dest_data in SEED_DESTINATIONS:
        country_name = dest_data["country"]
        country = db.query(Country).filter(Country.name == country_name).first()
        if not country:
            country = Country(
                name=country_name,
                code=dest_data["country_code"],
                currency_code=dest_data["currency"],
                currency_symbol=dest_data["currency_symbol"]
            )
            db.add(country)
            db.flush()

        destination = Destination(
            name=dest_data["name"],
            country_id=country.id,
            tagline=dest_data["tagline"],
            description=dest_data["description"],
            hero_image=dest_data["hero_image"],
            thumbnail=dest_data["thumbnail"],
            approx_daily_budget=dest_data["approx_daily_budget"],
            currency=dest_data["currency"],
            best_time_to_visit=dest_data["best_time_to_visit"],
            is_featured=dest_data["is_featured"],
            trending_score=dest_data["trending_score"]
        )

        # Attach interests
        for int_name in dest_data["interests"]:
            if int_name in interest_map:
                destination.interests.append(interest_map[int_name])

        # Attach travel types
        for tt_name in dest_data["travel_types"]:
            if tt_name in travel_type_map:
                destination.travel_types.append(travel_type_map[tt_name])

        db.add(destination)
        db.flush()

        # Seed Attractions
        for attr in dest_data["attractions"]:
            db.add(Attraction(
                destination_id=destination.id,
                name=attr["name"],
                category=attr["category"],
                description=attr["description"],
                estimated_duration_hours=attr["estimated_duration_hours"],
                estimated_cost=attr["estimated_cost"],
                best_time_of_day=attr.get("best_time_of_day"),
                location_area=attr.get("location_area")
            ))

        # Seed Local Services
        for svc in dest_data["local_services"]:
            db.add(LocalService(
                destination_id=destination.id,
                category=svc["category"],
                name=svc["name"],
                purpose=svc["purpose"],
                platform=svc.get("platform", "iOS / Android"),
                explanation=svc["explanation"],
                app_link=svc.get("app_link", ""),
                recommended=svc.get("recommended", True)
            ))

        # Seed Culture Guides
        for cult in dest_data["culture_guides"]:
            db.add(CultureGuide(
                destination_id=destination.id,
                category=cult["category"],
                title=cult["title"],
                description=cult["description"],
                importance_level=cult.get("importance_level", "Standard")
            ))

        # Seed Safety Info
        for safe in dest_data["safety_info"]:
            db.add(SafetyInfo(
                destination_id=destination.id,
                category=safe["category"],
                title=safe["title"],
                description=safe["description"],
                severity=safe.get("severity", "Notice")
            ))

        # Seed Emergency Contacts
        for emerg in dest_data["emergency_contacts"]:
            db.add(EmergencyContact(
                destination_id=destination.id,
                service_type=emerg["service_type"],
                contact_number=emerg["contact_number"],
                notes=emerg.get("notes")
            ))

    db.commit()
