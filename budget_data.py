# Starting data for the wedding budget planner.
# The last three expenses are deliberately broken so the program can show
# how it reports bad data and skips it.

TOTAL_BUDGET = 20000

EXPENSES = [
    {"category": "Venue", "description": "Reception hall hire", "estimated": 7000, "actual": 7500},
    {"category": "Catering", "description": "Dinner for 100 guests", "estimated": 5000, "actual": 5800},
    {"category": "Catering", "description": "Wedding cake", "estimated": 600, "actual": 550},
    {"category": "Photography", "description": "Photographer full day", "estimated": 2500, "actual": 2000},
    {"category": "Attire", "description": "Wedding dress", "estimated": 1800, "actual": 2100},
    {"category": "Attire", "description": "Suit hire", "estimated": 400, "actual": 300},
    {"category": "Flowers", "description": "Bouquets and centrepieces", "estimated": 1200, "actual": 1150},
    {"category": "Music", "description": "DJ for the evening", "estimated": 900, "actual": 1000},
    {"category": "Decor", "description": "Table decorations", "estimated": 600, "actual": 450},
    {"category": "Transport", "description": "Vintage car", "estimated": 350, "actual": -50},
    {"category": "Stationery", "description": "Invitations", "estimated": 300},
    {"category": "Favours", "description": "Guest gifts", "estimated": "two hundred", "actual": 180},
]