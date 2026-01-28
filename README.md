# Kooli tunniplaani ja Google'i kalendri sunkroonimine

See projekt on loodud kooli tunniplaani automaatseks kogumiseks ja selle lisamiseks Google'i kalendrisse. Programm loeb andmeid kooli veebilehelt ja loob vastavad sundmused sinu kalendrisse.

## Kasutamine

1. Paigalda vajalikud teegid:
   ```bash
   pip install -r requirements.txt
   ```
2. Seadista Google Cloud Console'is uus projekt ja laadi alla `credentials.json` fail.
3. Lisa `credentials.json` projekti juurkausta.
4. Muuda failis `config.py` oma kooli andmeid (vaata allpool).
5. Kaivita programm:
   ```bash
   python main.py
   ```

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

1. Install the required libraries using:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up a new project in the Google Cloud Console and download the `credentials.json` file.
3. Place the `credentials.json` file in the project's root directory.
4. Edit your school's details in `config.py` (see below).
5. Run the program using:
   ```bash
   python main.py
   ```

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
