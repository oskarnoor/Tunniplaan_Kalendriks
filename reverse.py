from calendar_api import get_calendar_service, delete_synced_events
from config import CALENDAR_ID
from scraper import parse_lesson_plan
import sys

def main():
    print("This script will remove events added by the School Lesson Sync.")
    service = get_calendar_service()
    if not service:
        print("Failed to connect to Google Calendar.")
        return

    # Option 1: Try to get the range from the current lesson plan (most precise)
    try:
        print("Fetching current lesson plan range for targeted removal...")
        lessons_data = parse_lesson_plan()
        start_date = lessons_data['start_date']
        end_date = lessons_data['end_date']
        
        print(f"Targeting range: {start_date.date()} to {end_date.date()}")
        delete_synced_events(service, CALENDAR_ID, start_date, end_date)
        
    except Exception as e:
        print(f"Could not fetch lesson plan range: {e}")
        print("Falling back to broad search (past 30 days to next 180 days)...")
        delete_synced_events(service, CALENDAR_ID)

    print("\nRemoval complete!")

if __name__ == "__main__":
    main()
