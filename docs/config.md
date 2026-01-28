# Configuration Documentation (`config.py`)

The `config.py` file contains all the settings and mappings required for the School Lesson Plan to Google Calendar sync project.

## General Settings

| Variable | Description | Example |
| :--- | :--- | :--- |
| `LESSON_PLAN_URL` | The URL to your specific class's HTML lesson plan. | `"https://real.edu.ee/.../d5pe1A_10A.htm"` |
| `TIMETABLE_URL` | The URL to the school's general timetable page (used for lesson times). | `"https://real.edu.ee/oppimine/tunniplaan/tunnid-harju/"` |
| `CALENDAR_ID` | The ID of the Google Calendar where events will be synced. Use `'primary'` for your main calendar. | `'primary'` |
| `TIMETABLE_CATEGORY` | The specific class group name to look for on the timetable page. | `"9.–10. klass"` |
| `DEFAULT_YEAR` | The fallback year if extraction from the HTML title fails. | `2026` |

## Lesson Mappings (`LESSON_MAPPINGS`)

This dictionary maps short lesson abbreviations found in the HTML to full, human-readable names.
- **Key**: Abbreviation (e.g., `"M"`)
- **Value**: Full Name (e.g., `"Matemaatika"`)

Example:
```python
LESSON_MAPPINGS = {
    "M": "Matemaatika",
    "EK": "Eesti Keel",
    "KK": "Kehalinekasvatus",
    # ...
}
```

## Visibility Settings (`SHOW_LESSONS`)

Allows users to toggle specific lessons on or off. If a lesson abbreviation exists at the start of a cell and its value is `False`, it will be skipped entirely.

Example:
```python
SHOW_LESSONS = {
    "Koor": False,  # Will not be added to calendar
    "Prog": True    # Will be added to calendar
}
```

## Group Selection (`SELECTED_GROUPS`)

Used for lessons divided into groups (e.g., Language groups).
- **Key**: Language prefix (`"IK"`, `"VK"`)
- **Value**: The group number you belong to (e.g., `1` or `2`).

The scraper checks if your selected group number is present in the lesson string (e.g., `IK1` matches group `1`).

## Teacher Selection (`SELECTED_TEACHERS`)

Used when multiple teachers offer the same lesson at the same time (e.g., Sports/Kehaline kasvatus).
- **Key**: Lesson abbreviation (`"KK"`)
- **Value**: The teacher's name or a unique substring of it.

Example:
```python
SELECTED_TEACHERS = {
    "KK": "MSonge"
}
```
Only lessons containing the specified teacher's name in that slot will be kept.
