# router.py

from datetime import datetime
import json
import re


# ============================================================
# CURRENT DATE / TIME
# ============================================================

def get_current_datetime():
    """
    Get the current local date and time.

    The machine's local timezone is used.
    For your Mumbai project, make sure Windows is set to
    India Standard Time.
    """
    return datetime.now()


def get_current_date():
    return get_current_datetime().strftime("%Y-%m-%d")


def get_current_hour():
    return get_current_datetime().hour


# ============================================================
# DATE EXTRACTION
# ============================================================

def extract_date(query):
    """
    Extract date from the user's query.

    If no date is mentioned, use today's date.
    """

    query_lower = query.lower()

    # --------------------------------------------------------
    # Today
    # --------------------------------------------------------

    if "today" in query_lower:
        return get_current_date()

    # --------------------------------------------------------
    # Tomorrow
    # --------------------------------------------------------

    if "tomorrow" in query_lower:
        from datetime import timedelta

        tomorrow = get_current_datetime() + timedelta(days=1)

        return tomorrow.strftime("%Y-%m-%d")

    # --------------------------------------------------------
    # Yesterday
    # --------------------------------------------------------

    if "yesterday" in query_lower:
        from datetime import timedelta

        yesterday = get_current_datetime() - timedelta(days=1)

        return yesterday.strftime("%Y-%m-%d")

    # --------------------------------------------------------
    # YYYY-MM-DD
    # --------------------------------------------------------

    match = re.search(
        r"\b(20\d{2}-\d{1,2}-\d{1,2})\b",
        query
    )

    if match:
        return match.group(1)

    # --------------------------------------------------------
    # DD/MM/YYYY
    # --------------------------------------------------------

    match = re.search(
        r"\b(\d{1,2})/(\d{1,2})/(20\d{2})\b",
        query
    )

    if match:

        day = int(match.group(1))
        month = int(match.group(2))
        year = int(match.group(3))

        return f"{year:04d}-{month:02d}-{day:02d}"

    # --------------------------------------------------------
    # No date mentioned
    # → Use current date
    # --------------------------------------------------------

    return get_current_date()


# ============================================================
# TIME EXTRACTION
# ============================================================

def extract_hour(query):
    """
    Extract hour from the user's query.

    If no hour is mentioned, use the current hour.
    """

    query_lower = query.lower()

    # --------------------------------------------------------
    # "5 PM", "5pm", "5:30 PM"
    # --------------------------------------------------------

    match = re.search(
        r"\b(\d{1,2})(?::(\d{2}))?\s*(am|pm)\b",
        query_lower
    )

    if match:

        hour = int(match.group(1))
        period = match.group(3)

        if period == "pm" and hour != 12:
            hour += 12

        if period == "am" and hour == 12:
            hour = 0

        return hour

    # --------------------------------------------------------
    # "17:00", "19:30"
    # --------------------------------------------------------

    match = re.search(
        r"\b([01]?\d|2[0-3]):[0-5]\d\b",
        query
    )

    if match:
        return int(match.group(1))

    # --------------------------------------------------------
    # No time mentioned
    # → Current hour
    # --------------------------------------------------------

    return get_current_hour()


# ============================================================
# AREA EXTRACTION
# ============================================================

MUMBAI_AREAS = [
    "Andheri",
    "Bandra",
    "Powai",
    "Kurla",
    "Borivali",
    "Dadar",
    "Goregaon",
    "Malad",
    "Mulund",
    "Thane",
    "Vile Parle",
    "Santacruz",
    "Chembur",
    "Worli",
    "Colaba",
    "Fort",
    "Lower Parel",
    "Ghatkopar",
    "Sion",
    "Matunga"
]


def extract_area(query):
    """
    Find a known Mumbai area in the query.
    """

    query_lower = query.lower()

    for area in MUMBAI_AREAS:

        if area.lower() in query_lower:
            return area

    return None


# ============================================================
# ROAD EXTRACTION
# ============================================================

def extract_road_name(query):
    """
    Try to extract a road name.

    Returns None if the user didn't provide one.
    """

    patterns = [
        r"(?:on|at|near)\s+([A-Za-z0-9 .'-]+?)\s+(?:road|rd)\b",
        r"([A-Za-z0-9 .'-]+?)\s+(?:road|rd)\b"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            query,
            re.IGNORECASE
        )

        if match:

            road = match.group(1).strip()

            return road

    return None


# ============================================================
# WEATHER EXTRACTION
# ============================================================

def extract_weather(query):
    """
    Extract weather if mentioned.
    """

    query_lower = query.lower()

    weather_keywords = {
        "rain": "Rain",
        "rainy": "Rain",
        "storm": "Storm",
        "cloudy": "Cloudy",
        "sunny": "Sunny",
        "clear": "Clear",
        "fog": "Fog"
    }

    for keyword, value in weather_keywords.items():

        if keyword in query_lower:
            return value

    # Default
    return "Clear"


# ============================================================
# EVENT EXTRACTION
# ============================================================

def extract_event(query):
    """
    Extract event information if mentioned.
    """

    query_lower = query.lower()

    events = [
        "festival",
        "concert",
        "cricket match",
        "football match",
        "match",
        "event",
        "holiday",
        "protest",
        "accident"
    ]

    for event in events:

        if event in query_lower:
            return event.title()

    return "None"


# ============================================================
# INTENT DETECTION
# ============================================================

def detect_intent(query):
    """
    Determine what the user wants.
    """

    q = query.lower()

    # --------------------------------------------------------
    # Traffic
    # --------------------------------------------------------

    traffic_keywords = [
        "traffic",
        "congestion",
        "congested",
        "vehicle",
        "vehicles",
        "road condition",
        "traffic condition",
        "traffic level"
    ]

    if any(word in q for word in traffic_keywords):
        return "traffic"

    # --------------------------------------------------------
    # AQI
    # --------------------------------------------------------

    aqi_keywords = [
        "aqi",
        "air quality",
        "pollution",
        "pm2.5",
        "pm10",
        "air pollution"
    ]

    if any(word in q for word in aqi_keywords):
        return "aqi"

    # --------------------------------------------------------
    # Complaints
    # --------------------------------------------------------

    complaint_keywords = [
        "complaint",
        "complaints",
        "citizen satisfaction",
        "satisfaction",
        "citizen complaint"
    ]

    if any(word in q for word in complaint_keywords):
        return "complaints"

    # --------------------------------------------------------
    # RAG / Knowledge
    # --------------------------------------------------------

    rag_keywords = [
        "what is",
        "what are",
        "explain",
        "define",
        "meaning",
        "how does",
        "why",
        "guideline",
        "guidelines",
        "information",
        "policy"
    ]

    if any(word in q for word in rag_keywords):
        return "rag"

    # --------------------------------------------------------
    # General
    # --------------------------------------------------------

    return "general"


# ============================================================
# MAIN ROUTER
# ============================================================

def route_query(query):
    """
    Understand the user's natural-language query.

    Responsibilities:

    1. Detect intent
    2. Extract entities
    3. Fill missing date with current date
    4. Fill missing hour with current hour
    5. Return structured information for the agent
    """

    if not query or not query.strip():

        return {
            "intent": "general",
            "query": query,
            "date": get_current_date(),
            "hour": get_current_hour()
        }

    # --------------------------------------------------------
    # Intent
    # --------------------------------------------------------

    intent = detect_intent(query)

    # --------------------------------------------------------
    # Entities
    # --------------------------------------------------------

    area = extract_area(query)

    road_name = extract_road_name(query)

    date = extract_date(query)

    hour = extract_hour(query)

    weather = extract_weather(query)

    event = extract_event(query)

    # --------------------------------------------------------
    # Build result
    # --------------------------------------------------------

    result = {
        "intent": intent,

        "query": query,

        "area": area,

        "road_name": road_name,

        "date": date,

        "hour": hour,

        "weather": weather,

        "event": event
    }

    return result


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_queries = [

        "What's the traffic like in Andheri?",

        "How is traffic in Bandra at 5 PM?",

        "What is the AQI?",

        "What was the AQI yesterday?",

        "What is the air quality today?",

        "Traffic in Powai tomorrow",

        "What causes traffic congestion?",

        "Explain AQI",

        "Tell me about citizen complaints"
    ]

    print("\nSMART CITY ROUTER TEST\n")

    for query in test_queries:

        print("-" * 60)

        print("QUERY:")
        print(query)

        result = route_query(query)

        print("\nROUTED DATA:")

        print(
            json.dumps(
                result,
                indent=4
            )
        )