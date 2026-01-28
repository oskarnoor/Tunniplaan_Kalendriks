import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
import pytz

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("Error: 'credentials.json' not found. Please follow the instructions to set up Google Calendar API.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def delete_synced_events(service, calendar_id, start_dt=None, end_dt=None):
    """Deletes events that were created by this script. 
    If start_dt and end_dt are provided, it limits the search to that range.
    Otherwise, it searches from 1 month ago to 6 months in the future.
    """
    if not start_dt:
        start_dt = datetime.now() - timedelta(days=30)
    if not end_dt:
        end_dt = datetime.now() + timedelta(days=180)

    print(f"Searching for school events to remove from {start_dt.date()} to {end_dt.date()}...")
    
    # We use a page-based approach to ensure we get all events if there are many
    events = []
    page_token = None
    while True:
        events_result = service.events().list(
            calendarId=calendar_id, 
            timeMin=start_dt.isoformat() + 'Z',
            timeMax=end_dt.isoformat() + 'Z',
            singleEvents=True,
            pageToken=page_token
        ).execute()
        events.extend(events_result.get('items', []))
        page_token = events_result.get('nextPageToken')
        if not page_token:
            break
    
    count = 0
    for event in events:
        if 'description' in event and 'School Lesson Sync' in event['description']:
            service.events().delete(calendarId=calendar_id, eventId=event['id']).execute()
            count += 1
    
    print(f"Removed {count} events.")

def clear_events_in_range(service, calendar_id, start_dt, end_dt):
    """Deletes events that were created by this script in the given range."""
    delete_synced_events(service, calendar_id, start_dt, end_dt)

def create_lesson_event(service, calendar_id, summary, start_iso, end_iso):
    event = {
        'summary': summary,
        'description': 'School Lesson Sync',
        'start': {
            'dateTime': start_iso,
            'timeZone': 'Europe/Tallinn',
        },
        'end': {
            'dateTime': end_iso,
            'timeZone': 'Europe/Tallinn',
        },
    }
    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print(f'Event created: {event.get("htmlLink")}')

def sync_lessons(lessons_data, calendar_id='primary'):
    service = get_calendar_service()
    if not service:
        return

    start_date = lessons_data['start_date']
    end_date = lessons_data['end_date']
    lessons = lessons_data['lessons']

    # Clear old events first
    # Offset end date to include the last day fully
    clear_end = end_date + timedelta(days=1)
    clear_events_in_range(service, calendar_id, start_date, clear_end)

    print(f"Syncing {len(lessons)} lesson patterns...")
    
    # Iterate through all days in the range
    current_date = start_date
    tz = pytz.timezone('Europe/Tallinn')
    
    while current_date <= end_date:
        day_of_week = current_date.weekday() # 0-6 (Mon-Sun)
        
        # Find lessons for this day of week
        daily_lessons = [l for l in lessons if l['day_idx'] == day_of_week]
        
        for l in daily_lessons:
            # Construct start and end datetimes
            start_h, start_m = map(int, l['start_time'].split(':'))
            end_h, end_m = map(int, l['end_time'].split(':'))
            
            start_dt = current_date.replace(hour=start_h, minute=start_m, second=0, microsecond=0)
            end_dt = current_date.replace(hour=end_h, minute=end_m, second=0, microsecond=0)
            
            # Localize and convert to ISO
            start_iso = tz.localize(start_dt).isoformat()
            end_iso = tz.localize(end_dt).isoformat()
            
            create_lesson_event(service, calendar_id, l['content'], start_iso, end_iso)
            
        current_date += timedelta(days=1)

    print("Sync complete!")
