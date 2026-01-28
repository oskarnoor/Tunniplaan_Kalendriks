# Configuration for the School Lesson Plan to Google Calendar sync

# The link to your specific class lesson plan
LESSON_PLAN_URL = "https://real.edu.ee/oppetoo/tunniplaan/......"

# The link to the general timetable (for lesson times)
TIMETABLE_URL = "https://real.edu.ee/oppimine/tunniplaan/tunnid-harju/"

# Google Calendar ID to sync to. 'primary' is your main calendar.
CALENDAR_ID = 'primary'

# Lesson category to look for in timetable (e.g., "9.–10. klass", "1.–4. klass", etc.)
TIMETABLE_CATEGORY = "9.–10. klass"

# Year extraction might be needed if not present in the lesson plan text
# The script will try to extract it from the lesson plan text first.
DEFAULT_YEAR = 2026

# Lesson name mappings
LESSON_MAPPINGS = {
    "Mv": "Matemaatikavalik",
    "M": "Matemaatika",
    "KK": "Kehalinekasvatus",
    "EK": "Eesti Keel",
    "A": "Ajalugu",
    "Fv": "Füüsikavalik",
    "PK": "Prantsuse keel",
    "SK": "Saksa keel",
    "IK": "Inglise keel",
    "VK": "Vene keel",
    "MU": "Muusika",
    "Klj": "Klassijuhatajatund",
    "Koor": "Koor",
    "Maj": "Majandus",
    "Prog": "Programeerimine",
    "IT": "Informaatika"
}

# Visibility settings for optional lessons
SHOW_LESSONS = {
    "Koor": False,
    "Maj": False,
    "Prog": False,
    "VK": False,
    "SK": False,
    "PK": False
}

# Group selection for divided lessons (e.g., 1 or 2)
# This applies to IK and VK mainly
SELECTED_GROUPS = {
    "IK": 1,
    "VK": 1,
    "IT": 1
}

# Teacher selection for specific lessons (e.g., Kehalinekasvatus)
# Specify the teacher's name or a substring of it.
SELECTED_TEACHERS = {
    "Lesson": "Teacher name in plan"
}
