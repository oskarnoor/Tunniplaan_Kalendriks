# Calendar API Documentation (`calendar_api.py`)

This module handles communication with the Google Calendar API, including authentication and event synchronization.

## Authentication Logic

### `get_calendar_service()`
- **Scopes**: Uses `'https://www.googleapis.com/auth/calendar'`.
- **`token.json`**: Stores user's access/refresh tokens after the first login.
- **`credentials.json`**: Required file containing the Google Cloud Project OAuth Client ID.
- **Flow**:
    1. Checks for `token.json`.
    2. If missing or invalid, triggers `InstalledAppFlow` to open a browser for login.
    3. Saves the new token back to `token.json`.

## Event Management

### `delete_synced_events(service, calendar_id, start_dt, end_dt)`
Finds and removes events created by this tool to prevent duplicates.
- **Identification**: Searches for the string `"School Lesson Sync"` in the event description.
- **Range**: Searches within the provided `start_dt` and `end_dt`. If not provided, defaults to -30 days to +180 days.
- **Pagination**: Uses `nextPageToken` to handle calendars with many events.

### `create_lesson_event(service, calendar_id, summary, start_iso, end_iso)`
Creates a single calendar event.
- **Timezone**: Hardcoded to `'Europe/Tallinn'`.
- **Description**: tagged with `"School Lesson Sync"` for future identification.

## Synchronization Workflow

### `sync_lessons(lessons_data, calendar_id)`
1. **Clearance**: Calls `clear_events_in_range` to delete all previously synced events within the new plan's date range.
2. **Iteration**: Steps through every day from `start_date` to `end_date`.
3. **Weekly Match**: For each day, it selects lessons from the `lessons_data` list that match the current day of the week (`day_idx`).
4. **Time Construction**: Combines the current loop date with the lesson's start/end times.
5. **API Calls**: Sends a request to Google Calendar to create each event.
