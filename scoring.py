"""
Scoring engine for the Ravel travel questionnaire.
"""

CATEGORIES = {
    "Adventure":   ["Q1",  "Q2",  "Q3",  "Q4",  "Q5"],
    "Budget":      ["Q6",  "Q7",  "Q8",  "Q9",  "Q10"],
    "Culture":     ["Q11", "Q12", "Q13", "Q14", "Q15"],
    "Relaxation":  ["Q16", "Q17", "Q18", "Q19", "Q20"],
    "Food":        ["Q21", "Q22", "Q23", "Q24", "Q25"],
    "Shopping":    ["Q26", "Q27", "Q28", "Q29"],
}


def calculate_scores(responses: dict, categories: dict) -> dict:
    """
    Average the Likert responses per category.

    Args:
        responses: {question_id: int (1–5)}
        categories: {category_name: [question_ids]}

    Returns:
        {category_name: float}
    """
    scores = {}
    for category, questions in categories.items():
        values = [responses[q] for q in questions if q in responses]
        scores[category] = sum(values) / len(values) if values else 0.0
    return scores


# ---------------------------------------------------------------------------
# Traveler-type definitions
# ---------------------------------------------------------------------------

TRAVELER_TYPES = [
    {
        "name": "The Adventurer",
        "description": "You crave excitement, love the unknown, and thrive in the wild. Bucket-list treks, extreme sports, and remote destinations are your playground.",
        "primary": "Adventure",
        "secondary": None,
    },
    {
        "name": "The Budget Explorer",
        "description": "You believe the best trips don't have to cost a fortune. You're resourceful, flexible, and know how to stretch every dollar.",
        "primary": "Budget",
        "secondary": None,
    },
    {
        "name": "The Cultural Connoisseur",
        "description": "History, art, and local traditions draw you in. You travel to understand the world, not just see it.",
        "primary": "Culture",
        "secondary": None,
    },
    {
        "name": "The Wellness Wanderer",
        "description": "Travel is your reset button. You seek tranquility, comfort, and experiences that restore mind and body.",
        "primary": "Relaxation",
        "secondary": None,
    },
    {
        "name": "The Culinary Nomad",
        "description": "Your itinerary is built around meals. From street food to Michelin stars, you eat your way through every destination.",
        "primary": "Food",
        "secondary": None,
    },
    {
        "name": "The Style Traveler",
        "description": "You blend retail therapy with wanderlust. Markets, boutiques, and local crafts are as important as the sights.",
        "primary": "Shopping",
        "secondary": None,
    },
    # --- Hybrid types (top-2 combinations) ---
    {
        "name": "The Thrill-Seeker Foodie",
        "description": "Extreme experiences by day, exceptional dining by night — you want intensity in all its forms.",
        "primary": "Adventure",
        "secondary": "Food",
    },
    {
        "name": "The Cultured Foodie",
        "description": "You immerse yourself in a destination's history and its cuisine, treating every meal as a cultural lesson.",
        "primary": "Culture",
        "secondary": "Food",
    },
    {
        "name": "The Luxury Escapist",
        "description": "You believe quality matters. Comfort, fine dining, and beautifully curated experiences define your ideal trip.",
        "primary": "Relaxation",
        "secondary": "Food",
    },
    {
        "name": "The Savvy Culturalist",
        "description": "You want rich cultural experiences without breaking the bank. Free museums, street art, and local neighbourhoods are your sweet spots.",
        "primary": "Culture",
        "secondary": "Budget",
    },
]


def classify_traveler(scores: dict) -> tuple[str, str, str]:
    """
    Classify a traveler based on their scores.

    Returns:
        (traveler_type_name, description, dominant_category)
    """
    sorted_categories = sorted(scores, key=scores.get, reverse=True)
    top1 = sorted_categories[0]
    top2 = sorted_categories[1] if len(sorted_categories) > 1 else None

    # Check for a hybrid type first (both top categories match)
    if top2 and scores[top2] >= 3.5:
        for t in TRAVELER_TYPES:
            if t["secondary"] and (
                (t["primary"] == top1 and t["secondary"] == top2)
                or (t["primary"] == top2 and t["secondary"] == top1)
            ):
                return t["name"], t["description"], top1

    # Fall back to single-dominant type
    for t in TRAVELER_TYPES:
        if t["secondary"] is None and t["primary"] == top1:
            return t["name"], t["description"], top1

    return "The Explorer", "You're a well-rounded traveler with a passion for discovery.", top1
