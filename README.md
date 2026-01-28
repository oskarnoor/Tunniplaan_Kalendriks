# Kooli tunniplaani ja Google'i kalendri sunkroonimine

See projekt on loodud kooli tunniplaani automaatseks kogumiseks ja selle lisamiseks Google'i kalendrisse. Programm loeb andmeid kooli veebilehelt ja loob vastavad sundmused sinu kalendrisse.

## Kasutamine

1. Paigalda vajalikud teegid:
   ```bash
   pip install -r requirements.txt
   ```
2. Seadista Google Calendar API (vt [Google'i kalendri API seadistamine](#googlei-kalendri-api-seadistamine) allpool).
3. Lisa `credentials.json` projekti juurkausta.
4. Muuda failis `config.py` oma kooli andmeid.
5. Kaivita programm:
   ```bash
   python main.py
   ```
   *Esmakordsel käivitamisel pead andma rakendusele loa oma kalendrit kasutada.*

## Seadistamine

Kogu seadistamine toimub failis `config.py`. Seal saad maarata:

### Kooli URL-id
- `LESSON_PLAN_URL`: Link sinu klassi tunniplaanile.
- `TIMETABLE_URL`: Link uldisele tunniplaanile, kus on tundide ajad.
- `TIMETABLE_CATEGORY`: Sinu klassiaste (naited: "9.-10. klass").

### Tundide nimetused
`LESSON_MAPPINGS` on sonastik, mis teisendab luhendid pikemateks nimedeks. Naited:
```python
LESSON_MAPPINGS = {
    "M": "Matemaatika",
    "EK": "Eesti Keel",
    "F": "Fuusika",      # Lisa oma luhendid siia
    "K": "Keemia",
}
```

### Valikulised tunnid
`SHOW_LESSONS` maarab, milliseid valikulisi tunde kuvada. Sea `True` kuvamiseks ja `False` peitmiseks:
```python
SHOW_LESSONS = {
    "Koor": False,   # Ei kuva koori
    "Prog": True,    # Kuva programmeerimist
}
```

### Ruhmad ja opetajad
- `SELECTED_GROUPS`: Kui tunnid on jagatud ruhmadesse (nt IK1, IK2), maarake oma ruhm.
- `SELECTED_TEACHERS`: Kui tunnil on mitu opetajat, maarake oma opetaja nimi.

## Google'i kalendri API seadistamine

Selle skripti kasutamiseks pead seadistama Google Cloudi projekti ja lubama kalendri API:

1. **Loo projekt:**
   - Mine [Google Cloud Console](https://console.cloud.google.com/) lehele.
   - Loo uus projekt (nupp "New Project").
2. **Luba API:**
   - Navigeeri **APIs & Services > Library**.
   - Otsi "Google Calendar API" ja klõpsa **Enable**.
3. **Seadista OAuth nõusoleku ekraan (Consent Screen):**
   - Vali **APIs & Services > OAuth consent screen**.
   - Vali tüübiks **External** ja vajuta **Create**.
   - Täida kohustuslikud väljad (App name, Support email, Developer email).
   - Jätka kuni sektsioonini **Test users** ja lisa sinna oma Google'i e-posti aadress. See on kriitiline samm!
4. **Loo mandaadid (Credentials):**
   - Vali **APIs & Services > Credentials**.
   - Klõpsa **Create Credentials > OAuth client ID**.
   - Vali rakenduse tüübiks **Desktop app**.
   - Pärast loomist laadi alla JSON-fail.
5. **Faili ettevalmistamine:**
   - Nimeta laaditud fail ümber: `credentials.json`.
   - Aseta see fail sellesse samasse kausta, kus asub `main.py`.

Pärast neid samme loo programmiga esimene ühendus: `python main.py`. Avaneb brauseriaken, kus pead sisse logima ja lubama ligipääsu. Seejärel tekkib automaatselt `token.json` fail.

## Avaldamine GitHubis

Kui soovid projekti GitHubis jagada, kasuta abiskripti:
```bash
python publish_helper.py backup    # Salvesta isiklikud andmed
python publish_helper.py restore   # Taasta isiklikud andmed
```

---

# School Lesson Plan to Google Calendar Sync

This project is designed to automatically collect school lesson schedules and add them to your Google Calendar. The program reads data from the school's website and creates the corresponding events in your calendar.

## Usage

1. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up Google Calendar API (see [Google Calendar API Setup](#google-calendar-api-setup) below).
3. Place the `credentials.json` file in the project's root directory.
4. Edit your school's details in `config.py`.
5. Run the program:
   ```bash
   python main.py
   ```
   *On the first run, you will be prompted to authorize the application in your browser.*

## Configuration

All settings are managed in the `config.py` file. Here you can define:

### School URLs
- `LESSON_PLAN_URL`: The link to your class's lesson plan page.
- `TIMETABLE_URL`: The link to the general timetable page that shows lesson times.
- `TIMETABLE_CATEGORY`: Your grade level (example: "9.-10. klass").

### Lesson Name Mappings
`LESSON_MAPPINGS` is a dictionary that converts short abbreviations to full names. Examples:
```python
LESSON_MAPPINGS = {
    "M": "Mathematics",
    "EK": "Estonian Language",
    "F": "Physics",      # Add your own abbreviations here
    "K": "Chemistry",
}
```

### Optional Lessons
`SHOW_LESSONS` determines which optional lessons to display. Set `True` to show and `False` to hide:
```python
SHOW_LESSONS = {
    "Koor": False,   # Do not show choir
    "Prog": True,    # Show programming
}
```

### Groups and Teachers
- `SELECTED_GROUPS`: If lessons are divided into groups (like IK1, IK2), set your group number.
- `SELECTED_TEACHERS`: If a lesson has multiple teachers, set a part of your teacher's name.

## Google Calendar API Setup

To use this script, you need to set up a Google Cloud Project and enable the Calendar API:

1. **Create a Project:**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project (e.g., "School Calendar Sync").
2. **Enable the API:**
   - Navigate to **APIs & Services > Library**.
   - Search for "Google Calendar API" and click **Enable**.
3. **Configure OAuth Consent Screen:**
   - Go to **APIs & Services > OAuth consent screen**.
   - Choose **External** user type and click **Create**.
   - Fill in the required fields (App name, user support email, developer contact info).
   - In the **Test users** section, add your own Google email address. This is required for the authorization to work in testing mode.
4. **Create Credentials:**
   - Go to **APIs & Services > Credentials**.
   - Click **Create Credentials > OAuth client ID**.
   - Select **Desktop app** as the Application type.
   - Name it (e.g., "My Desktop Client") and click **Create**.
5. **Download and Rename:**
   - Download the JSON file for your new OAuth client.
   - Rename the downloaded file to `credentials.json` and place it in the root directory of this project.

### Authorization (token.json)
The first time you run `python main.py`, a browser window will open asking you to log in to your Google account. After you grant permission, a `token.json` file will be created automatically in your project folder. This file stores your access credentials for future runs.

## Removing Events

To remove all events added by this script from your calendar, run:
```bash
python reverse.py
```

## Publishing to GitHub

If you want to share this project on GitHub, use the helper script:
```bash
python publish_helper.py backup    # Save personal data to a file
python publish_helper.py restore   # Restore personal data from the file
```

The `backup` command saves your `token.json`, `credentials.json`, and `config.py` to a single `my_personal_data.json` file. Move this file out of the project folder before publishing. When you want to use your personal settings again, move the file back and run the `restore` command.

## Adding New Abbreviations

To add a new lesson abbreviation:

1. Open `config.py`.
2. Find the `LESSON_MAPPINGS` dictionary.
3. Add a new line with the abbreviation and full name:
   ```python
   "B": "Biology",
   ```
4. Save the file and run `python main.py` again.

## Adding Optional Lessons

To control whether an optional lesson appears in your calendar:

1. Open `config.py`.
2. Find the `SHOW_LESSONS` dictionary.
3. Add or modify an entry:
   ```python
   "NewLesson": True,   # Show this lesson
   "AnotherLesson": False,  # Hide this lesson
   ```

## Adding Group or Teacher Filters

If a lesson is divided into groups:

1. Open `config.py`.
2. Find `SELECTED_GROUPS` and add your group:
   ```python
   "IK": 2,   # I am in English group 2
   ```

If a lesson has multiple teachers:

1. Find `SELECTED_TEACHERS` and add the teacher's name:
   ```python
   "KK": "Smith",  # My PE teacher's name contains "Smith"
   ```
