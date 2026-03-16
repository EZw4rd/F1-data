
# Static track information for Formula 1 circuits
# Focusing on characteristics, overtaking, and 2026 specific insights

TRACK_INFO = {
    "Bahrain Grand Prix": {
        "CircuitName": "Bahrain International Circuit",
        "Location": "Sakhir",
        "Length_km": 5.412,
        "Turns": 15,
        "DRS_Zones": 3,
        "Characteristics": ["Abrasive track surface", "High tire degradation", "Desert crosswinds", "Heavy braking zones"],
        "Overtaking": "Excellent. Primary spots at Turn 1 and Turn 4.",
        "Strategy": "High tire wear demands multi-stop strategies. Undercut is powerful.",
        "FunFact": "The first F1 race held in the Middle East (2004).",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Bahrain_Circuit.webp"
    },
    "Saudi Arabian Grand Prix": {
        "CircuitName": "Jeddah Corniche Circuit",
        "Location": "Jeddah",
        "Length_km": 6.174,
        "Turns": 27,
        "DRS_Zones": 3,
        "Characteristics": ["Fastest street circuit", "Very narrow with close walls", "High-speed flowing sections"],
        "Overtaking": "Moderate. Best chances at Turn 1 and the Turn 27 hairpin.",
        "Strategy": "One-stop is common. High Safety Car probability due to narrow layout.",
        "FunFact": "Features the most corners (27) of any track on the F1 calendar.",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Saudi_Arabia_Circuit.webp"
    },
    "Australian Grand Prix": {
        "CircuitName": "Albert Park Circuit",
        "Location": "Melbourne",
        "Length_km": 5.278,
        "Turns": 14,
        "DRS_Zones": 4, # 2026 Straight Mode Zones: 5
        "Characteristics": ["Semi-permanent street circuit", "Fast and flowing since 2022", "Historically bumpy"],
        "Overtaking": "Challenging. Turn 3 and Turn 11 are the key spots.",
        "Strategy": "Moderate tire wear. Safety gear logic is important for pit timing.",
        "FunFact": "The circuit circles Albert Park Lake and was significantly widened in 2022.",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Australia_Circuit.webp"
    },
    "Japanese Grand Prix": {
        "CircuitName": "Suzuka International Racing Course",
        "Location": "Suzuka",
        "Length_km": 5.807,
        "Turns": 18,
        "DRS_Zones": 1,
        "Characteristics": ["Figure-of-eight layout", "Iconic 130R and S-curves", "Highly technical"],
        "Overtaking": "Very difficult. The final chicane is the best realistic opportunity.",
        "Strategy": "High tire energy loads. Two-stop is typically faster than one-stop.",
        "FunFact": "Only figure-eight circuit in F1; designed originally as a Honda test track.",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Japan_Circuit.webp"
    },
    "Chinese Grand Prix": {
        "CircuitName": "Shanghai International Circuit",
        "Location": "Shanghai",
        "Length_km": 5.451,
        "Turns": 16,
        "DRS_Zones": 2,
        "Characteristics": ["Long 1.2km back straight", "Unique 'snail' corners", "Front-limited circuit"],
        "Overtaking": "High. Prime opportunity into Turn 14 via the long straight.",
        "Strategy": "Heavy emphasis on front-left tire management. Strategy-sensitive.",
        "FunFact": "Layout is inspired by the Chinese character 'shang' (上), meaning upwards.",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/China_Circuit.webp"
    },
    "Miami Grand Prix": {
        "CircuitName": "Miami International Autodrome",
        "Location": "Miami",
        "Length_km": 5.412,
        "Turns": 19,
        "DRS_Zones": 3,
        "Characteristics": ["Street-style around Hard Rock Stadium", "Long straights", "Technical Sector 3"],
        "Overtaking": "Good. Multiple DRS zones facilitate passing into Turns 1, 11, and 17.",
        "Strategy": "Surface can be slippery and abrasive. Heat plays a major factor.",
        "FunFact": "The 'marina' in the circuit's center is actually solid ground with painted water visuals.",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Miami_Circuit.webp"
    },
    "Emilia Romagna Grand Prix": {
        "CircuitName": "Autodromo Enzo e Dino Ferrari",
        "Location": "Imola",
        "Length_km": 4.909,
        "Turns": 19,
        "DRS_Zones": 1,
        "Characteristics": ["Old-school narrow track", "Anti-clockwise", "Technical and hilly"],
        "Overtaking": "Difficult. Turn 1 (Tamburello) after the main straight is the best spot.",
        "Strategy": "Qualifying is paramount. Hard to follow closely through the corners.",
        "FunFact": "One of the few tracks on the calendar run in an anti-clockwise direction.",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Emilia_Romagna_Circuit.webp"
    },
    "Monaco Grand Prix": {
        "CircuitName": "Circuit de Monaco",
        "Location": "Monte Carlo",
        "Length_km": 3.337,
        "Turns": 19,
        "DRS_Zones": 1,
        "Characteristics": ["Extremely narrow", "Slowest average speeds", "Zero margin for error"],
        "Overtaking": "Near impossible. Best chance is into Sainte-Devote or the Chicane.",
        "Strategy": "Track position is everything. One-stop is the only viable dry strategy.",
        "FunFact": "The track requires several thousand gear changes during the race distance.",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Monaco_Circuit.webp"
    },
    "Canadian Grand Prix": {
        "CircuitName": "Circuit Gilles-Villeneuve",
        "Location": "Montreal",
        "Length_km": 4.361,
        "Turns": 14,
        "DRS_Zones": 3,
        "Characteristics": ["Stop-start nature", "Heavy on brakes", "Close 'Wall of Champions'"],
        "Overtaking": "Very good. The hairpin and the final chicane are prime spots.",
        "Strategy": "Brake wear is a critical factor. High probability of Safety Cars.",
        "FunFact": "The circuit is located on a man-made island in the St. Lawrence River.",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Canada_Circuit.webp"
    },
    "Spanish Grand Prix": {
        "CircuitName": "Circuit de Barcelona-Catalunya",
        "Location": "Barcelona",
        "Length_km": 4.657,
        "Turns": 14,
        "DRS_Zones": 2,
        "Characteristics": ["Aerodynamically demanding", "High-speed final sector reinstated", "Tire killer"],
        "Overtaking": "Moderate. Removal of the final chicane has improved passing into Turn 1.",
        "Strategy": "High tire degradation. Strategies often revolve around managing the front tires.",
        "FunFact": "Used extensively for winter testing due to its mix of all corner types.",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Spain_Circuit.webp"
    },
    "Austrian Grand Prix": {
        "CircuitName": "Red Bull Ring",
        "Location": "Spielberg",
        "Length_km": 4.318,
        "Turns": 10,
        "DRS_Zones": 3,
        "Characteristics": ["Significant elevation changes", "Three long straights", "Shortest lap time"],
        "Overtaking": "Excellent. Turn 3 (uphill hairpin) and Turn 4 offer great action.",
        "Strategy": "Fast lap means many laps. Strategy involves staying in the DRS train.",
        "FunFact": "The track has the fewest corners (10) of any current F1 circuit.",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Austria_Circuit.webp"
    },
    "British Grand Prix": {
        "CircuitName": "Silverstone Circuit",
        "Location": "Silverstone",
        "Length_km": 5.891,
        "Turns": 18,
        "DRS_Zones": 2,
        "Characteristics": ["Ultra high-speed corners", "Iconic Maggots-Becketts-Chapel", "Flowing layout"],
        "Overtaking": "Good. Stowe and The Loop are common overtaking zones.",
        "Strategy": "Extremely high tire loads. Strategies can be affected by unpredictable UK weather.",
        "FunFact": "Hosted the first ever Formula 1 World Championship race in 1950.",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Great_Britain_Circuit.webp"
    },
    "Hungarian Grand Prix": {
        "CircuitName": "Hungaroring",
        "Location": "Budapest",
        "Length_km": 4.381,
        "Turns": 14,
        "DRS_Zones": 2,
        "Characteristics": ["Twisty 'Monaco without walls'", "Dusty and hot", "Constant succession of turns"],
        "Overtaking": "Difficult. Turn 1 remains the only prime spot for passing.",
        "Strategy": "Focus on high downforce. Undercut is very effective here.",
        "FunFact": "The track is built in a natural bowl, providing great views for spectators.",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Hungary_Circuit.webp"
    },
    "Belgian Grand Prix": {
        "CircuitName": "Circuit de Spa-Francorchamps",
        "Location": "Spa",
        "Length_km": 7.004,
        "Turns": 20,
        "DRS_Zones": 2,
        "Characteristics": ["Longest track on the calendar", "Iconic Eau Rouge/Raidillon", "Variable weather"],
        "Overtaking": "High. The Kemmel straight after Eau Rouge is a premier spot.",
        "Strategy": "Dynamic setup needed for straights vs. corners. Weather shifts fast.",
        "FunFact": "The circuit is so long it can be raining in one sector and dry in another.",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Belgium_Circuit.webp"
    },
    "Dutch Grand Prix": {
        "CircuitName": "Circuit Zandvoort",
        "Location": "Zandvoort",
        "Length_km": 4.259,
        "Turns": 14,
        "DRS_Zones": 2,
        "Characteristics": ["High banking at Turns 3 and 14", "Dunes and sand", "Narrow and technical"],
        "Overtaking": "Challenging. Banked T14 allows earlier DRS activation towards Turn 1.",
        "Strategy": "One-stop is primary. High-speed corners put huge energy into tires.",
        "FunFact": "Turn 3 uses a 'progressive' banking similar to American oval tracks.",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Netherlands_Circuit.webp"
    },
    "Italian Grand Prix": {
        "CircuitName": "Autodromo Nazionale Monza",
        "Location": "Monza",
        "Length_km": 5.793,
        "Turns": 11,
        "DRS_Zones": 2,
        "Characteristics": ["The 'Temple of Speed'", "Long straights", "Low downforce specialized"],
        "Overtaking": "Excllent. Prime spots at the Variante del Rettifilo (Turns 1-2).",
        "Strategy": "Lowest downforce of the year. Focus on top speed and braking stability.",
        "FunFact": "Oldest purpose-built motor racing venue in mainland Europe (1922).",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Italy_Circuit.webp"
    },
    "Azerbaijan Grand Prix": {
        "CircuitName": "Baku City Circuit",
        "Location": "Baku",
        "Length_km": 6.003,
        "Turns": 20,
        "DRS_Zones": 2,
        "Characteristics": ["Ultra-long 2.2km main straight", "Tight Castle section", "City street circuit"],
        "Overtaking": "High. The main straight and wide Turn 1 provide spectacular slipstreaming.",
        "Strategy": "Compromise setup for low drag vs technical castle section. High safety car rate.",
        "FunFact": "The Castle section is so narrow it requires slow-speed precision.",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Azerbaijan_Circuit.webp"
    },
    "Singapore Grand Prix": {
        "CircuitName": "Marina Bay Street Circuit",
        "Location": "Singapore",
        "Length_km": 4.940,
        "Turns": 19,
        "DRS_Zones": 4,
        "Characteristics": ["Night race", "Extremely humid", "Bump city streets"],
        "Overtaking": "Moderate. New layout and fourth DRS zone have improved passing.",
        "Strategy": "One-stop is common but requires extreme tire management. 100% Safety Car record.",
        "FunFact": "Drivers can lose up to 3kg of body weight during the race due to heat.",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Singapore_Circuit.webp"
    },
    "United States Grand Prix": {
        "CircuitName": "Circuit of The Americas",
        "Location": "Austin",
        "Length_km": 5.513,
        "Turns": 20,
        "DRS_Zones": 2,
        "Characteristics": ["Steep climb to Turn 1", "Sequences inspired by Silverstone", "Very bumpy surface"],
        "Overtaking": "Great. Turn 1 and the long back straight into Turn 12 are hot spots.",
        "Strategy": "Strategy varies based on track temperature and tire deg. High vertical G-loads.",
        "FunFact": "The climb to Turn 1 is so steep that drivers can't see the apex on entry.",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/USA_Circuit.webp"
    },
    "Mexico City Grand Prix": {
        "CircuitName": "Autodromo Hermanos Rodriguez",
        "Location": "Mexico City",
        "Length_km": 4.304,
        "Turns": 17,
        "DRS_Zones": 3,
        "Characteristics": ["Crucial high altitude", "Thin air (less drag and cooling)", "Stadium section"],
        "Overtaking": "Moderate. Very long run to Turn 1 allows for slipstreaming.",
        "Strategy": "Cooling is the biggest challenge. Thin air makes aero less effective.",
        "FunFact": "The circuit sits at over 2,200m above sea level.",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Mexico_Circuit.webp"
    },
    "Sao Paulo Grand Prix": {
        "CircuitName": "Autódromo José Carlos Pace",
        "Location": "Interlagos",
        "Length_km": 4.309,
        "Turns": 15,
        "DRS_Zones": 2,
        "Characteristics": ["Anti-clockwise and undulating", "Short but intense", "Passionate 'Torcida' fans"],
        "Overtaking": "Excellent. The Senna 'S' and the run into Turn 4 are legendary.",
        "Strategy": "Weather is a constant threat. Short lap time leads to busy pit lanes.",
        "FunFact": "Actually located within a natural amphitheater between two lakes.",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Brazil_Circuit.webp"
    },
    "Las Vegas Grand Prix": {
        "CircuitName": "Las Vegas Strip Circuit",
        "Location": "Las Vegas",
        "Length_km": 6.201,
        "Turns": 17,
        "DRS_Zones": 2,
        "Characteristics": ["Famous Strip straight", "Cold night temperatures", "Street circuit speed"],
        "Overtaking": "High. The 1.9km Strip straight allows for massive top speeds and passing.",
        "Strategy": "Tire warm-up is the biggest issue due to cold night air. High graining risk.",
        "FunFact": "Cars reach speeds comparable to Monza on the Las Vegas Strip.",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Las_Vegas_Circuit.webp"
    },
    "Qatar Grand Prix": {
        "CircuitName": "Lusail International Circuit",
        "Location": "Lusail",
        "Length_km": 5.419,
        "Turns": 16,
        "DRS_Zones": 1,
        "Characteristics": ["Fast and flowing technical corners", "Severe track limits", "Extreme heat"],
        "Overtaking": "Difficult. Mostly limited to the 1km main straight.",
        "Strategy": "Tire durability is critical. High-speed corners put huge stress on side-walls.",
        "FunFact": "Originally designed for MotoGP; resurfaced specifically for modern F1 cars in 2023.",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Qatar_Circuit.webp"
    },
    "Abu Dhabi Grand Prix": {
        "CircuitName": "Yas Marina Circuit",
        "Location": "Abu Dhabi",
        "Length_km": 5.281,
        "Turns": 16,
        "DRS_Zones": 2,
        "Characteristics": ["Twilight race", "Modified loop in 2021", "Hotel passing under"],
        "Overtaking": "Moderate. 2021 changes improved the flow and passing into Turn 5 and Turn 9.",
        "Strategy": "Sunset causes track temp to drop significantly during the race. One-stop is standard.",
        "FunFact": "The pit exit tunnel passes underneath the race track itself.",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Abu_Dhabi_Circuit.webp"
    }
}

def get_track_info(event_name):
    """Returns track info for a given event name, or None if not found."""
    # Try fuzzy match or direct match
    for name, info in TRACK_INFO.items():
        if name in event_name or event_name in name:
            return info
    return None
