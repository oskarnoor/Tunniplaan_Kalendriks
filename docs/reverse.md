# Reverse Sync Documentation (`reverse.py`)

The `reverse.py` script is a utility tool designed to clean up your calendar by removing all events added by the sync script.

## Functionality

The script searches for events containing the description `"School Lesson Sync"` and deletes them.

### Targeted Removal (Primary Strategy)
The script attempts to run `parse_lesson_plan()` to determine the exact date range of the current active plan. If successful, it only deletes events within that specific window.

### Broad Removal (Fallback)
If the lesson plan cannot be reached or parsed (e.g., the URL is broken), the script falls back to a broad search:
- **Range**: From **30 days ago** to **180 days in the future**.
- Any event found with the synchronization tag in this window will be removed.

## Usage
Run the script using Python:
```bash
python reverse.py
```

This is useful if you want to clear your calendar before changing configuration settings or if you no longer wish to have the school schedule synced.
