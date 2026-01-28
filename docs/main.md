# Main Script Documentation (`main.py`)

The `main.py` file is the primary entry point for the synchronization process. It orchestrates the flow between the scraper and the Google Calendar API.

## Execution Flow

1. **Scraping**: Calls `parse_lesson_plan()` from `scraper.py` to get the latest schedule data.
2. **Logging**: Prints the identified date range and the number of unique lesson patterns found.
3. **Synchronization**: Passes the scraped data to `sync_lessons()` in `calendar_api.py`.
4. **Error Handling**: Wrapped in a try/except block to catch and print errors during the fetch or sync phases.

## Usage
Simply run the script using Python:
```bash
python main.py
```

Ensure `credentials.json` is present in the root directory before running for the first time.
