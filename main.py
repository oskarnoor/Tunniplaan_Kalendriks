from scraper import parse_lesson_plan
from calendar_api import sync_lessons
from config import CALENDAR_ID

def main():
    print("Fetching lesson plan...")
    try:
        lessons_data = parse_lesson_plan()
        print(f"Period: {lessons_data['start_date'].date()} to {lessons_data['end_date'].date()}")
        print(f"Found {len(lessons_data['lessons'])} unique lesson slots in the plan.")
        
        print("\nStarting sync to Google Calendar...")
        sync_lessons(lessons_data, CALENDAR_ID)
        
    except Exception as e:
        print(f"Error during sync: {e}")

if __name__ == "__main__":
    main()
