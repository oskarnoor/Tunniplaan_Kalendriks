# Scraper Documentation (`scraper.py`)

The `scraper.py` module is responsible for fetching and parsing HTML content from the school's lesson plan and timetable websites.

## Core Functions

### `get_html(url)`
Fetches the raw HTML content from a URL.
- **Encoding**: Uses `response.apparent_encoding` to handle various charset distributions (common in Older HTML exports like Untis).
- **Error Handling**: Raises a `HTTPError` if the request fails.

### `parse_timetable_times()`
Extracts lesson start and end times from the general timetable.
- **Strategy**: 
    1. Searches for the `TIMETABLE_CATEGORY` (e.g., "9.–10. klass").
    2. Uses Regex (`(\d+)\.\s+(\d{2}:\d{2})\s*[–-]\s*(\d{2}:\d{2})`) to find time slots around that category.
    3. **Fallback**: If the category isn't found or parsing fails, it returns hardcoded default times (1-10) suitable for the specified school.

### `parse_lesson_plan()`
The main orchestration function for parsing the class-specific schedule.

#### 1. Date Extraction
- Searches the header for date ranges in format `DD.MM.YYYY - DD.MM.YYYY` or `DD.MM - DD.MM`.
- If only month/day is found, it uses the current year.

#### 2. Table Parsing
- Finds the schedule table by looking for the string "Esmaspäev".
- Extracts day names and maps them to indexes (0-4).

#### 3. Row-by-Row Processing
- Iterates through rows (lesson numbers).
- For each cell (day):
    - Splits text into blocks based on known abbreviations from `config.py`.
    - **Filtering Logic**:
        - **Groups**: Checks `SELECTED_GROUPS` for IK/VK lessons.
        - **Visibility**: Checks `SHOW_LESSONS`.
        - **Teachers**: Checks `SELECTED_TEACHERS` for specific lessons.
        - **Cleanup**: Discards blocks that don't start with a known subject abbreviation (e.g., stray room numbers).
    - **Mapping**: Replaces abbreviations with full names from `LESSON_MAPPINGS`.

#### 4. Deduplication
- Sorts lessons to process longer (more informative) blocks first.
- Prevents adding substrings as separate events in the same slot.

## Data Structure Returned
```json
{
    "start_date": datetime,
    "end_date": datetime,
    "lessons": [
        {
            "content": "Full Subject Name Room/Info",
            "day_idx": 0,
            "start_time": "08:00",
            "end_time": "08:45"
        }
    ]
}
```
