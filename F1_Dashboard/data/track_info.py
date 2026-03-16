
# Static track information for Formula 1 circuits
# Focusing on characteristics, overtaking, and 2026 specific insights

TRACK_INFO = {
    "Australian Grand Prix": {
        "CircuitName": "Albert Park Circuit",
        "Location": "Melbourne",
        "Length_km": 5.278,
        "Turns": 14,
        "DRS_Zones": 4, # 2026 Straight Mode Zones: 5
        "Characteristics": [
            "Semi-permanent street circuit",
            "High average speeds after 2022 modifications",
            "Fast and flowing layout",
            "Variable weather common"
        ],
        "Overtaking": "Challenging. Turn 3 is the most frequent spot. 2022 layout changes aimed to improve flow and passing.",
        "Strategy": "Moderate tire wear. Safety car probability is historically high. 2026 'Straight Mode' will be critical for managing energy on the five designated straights.",
        "FunFact": "The circuit circles Albert Park Lake and was significantly widened in 2022 to improve racing spectacle.",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Australia_Circuit.webp"
    },
    "Chinese Grand Prix": {
        "CircuitName": "Shanghai International Circuit",
        "Location": "Shanghai",
        "Length_km": 5.451,
        "Turns": 16,
        "DRS_Zones": 2, # 2026 Straight Mode Zones: 4
        "Characteristics": [
            "Inspired by the Chinese character 'shang' (上)",
            "Challenging Turn 1-3 complex (360-degree)",
            "One of the longest back straights in F1 (1.17km)",
            "Heavy emphasis on front-left tire management"
        ],
        "Overtaking": "Very good. The long back straight followed by heavy braking into Turn 14 is a prime spot.",
        "Strategy": "Strategy-sensitive track. High front-end demand. Front-limited circuit. Undercut can be very powerful here.",
        "FunFact": "The opening complex of corners (Turns 1, 2, and 3) is a unique tightening spiral that seems to never end.",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/China_Circuit.webp"
    },
    "Japanese Grand Prix": {
        "CircuitName": "Suzuka International Racing Course",
        "Location": "Suzuka",
        "Length_km": 5.807,
        "Turns": 18,
        "DRS_Zones": 1,
        "Characteristics": [
            "Only 'Figure-Of-Eight' circuit on the calendar",
            "Highly technical 'S' Curves in Sector 1",
            "Iconic 130R high-speed corner",
            "High G-force loads on drivers"
        ],
        "Overtaking": "Difficult. Requires precision and a mistake from the car ahead. The chicane at the end of the lap is the best chance.",
        "Strategy": "High tire degradation due to high-energy corners. Two-stop is common. Very driver-centric track.",
        "FunFact": "Suzuka's figure-eight layout means it has both clockwise and anti-clockwise sections!",
        "TrackMapUrl": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Japan_Circuit.webp"
    }
}

def get_track_info(event_name):
    """Returns track info for a given event name, or None if not found."""
    # Try fuzzy match or direct match
    for name, info in TRACK_INFO.items():
        if name in event_name or event_name in name:
            return info
    return None
