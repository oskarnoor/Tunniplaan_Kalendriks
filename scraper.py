import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
from config import (
    LESSON_PLAN_URL, TIMETABLE_URL, TIMETABLE_CATEGORY, 
    LESSON_MAPPINGS, SHOW_LESSONS, SELECTED_GROUPS, SELECTED_TEACHERS
)

def get_html(url):
    response = requests.get(url)
    response.raise_for_status()
    # Use 'latin-1' or 'utf-8' depending on the site; Untis often uses windows-1252 or latin-1
    # Let's try to detect or use what's common.
    response.encoding = response.apparent_encoding
    return response.text

def parse_timetable_times():
    """Parses lesson times from the timetable URL."""
    html = get_html(TIMETABLE_URL)
    soup = BeautifulSoup(html, 'html.parser')
    
    times = {}
    
    # Try finding the target text in any element
    target_node = soup.find(string=lambda t: TIMETABLE_CATEGORY in t)
    
    # Search the entire document first as a fallback for times
    all_text = soup.get_text()
    pattern = r"(\d+)\.\s+(\d{2}:\d{2})\s*[–-]\s*(\d{2}:\d{2})"
    
    if target_node:
        # Search specifically around the target node first
        search_root = target_node.parent
        content_around = ""
        curr = search_root
        for _ in range(10): 
            if not curr: break
            content_around += curr.get_text() + "\n"
            curr = curr.find_next()
        
        matches = re.findall(pattern, content_around)
        if matches:
            for match in matches:
                num, start, end = match
                times[int(num)] = (start, end)
            return times

    # Fallback: Search all text for the patterns. 
    # Note: This might get wrong times if multiple categories are visible.
    # But usually, it's better than nothing if we can't find the category element.
    matches = re.findall(pattern, all_text)
    if matches:
        # We only take the first set of 1-10 or similar
        # Since 10. klass is usually in the middle, we might need to be careful.
        # For now, let's use defaults if we are unsure, as they are correct for 10A anyway.
        pass

    print(f"Using default times for {TIMETABLE_CATEGORY}.")
    return {
        1: ("08:00", "08:45"), 2: ("08:55", "09:40"), 3: ("09:50", "10:35"),
        4: ("10:45", "11:30"), 5: ("12:00", "12:45"), 6: ("12:55", "13:40"),
        7: ("13:50", "14:35"), 8: ("14:45", "15:30"), 9: ("15:40", "16:25"),
        10: ("16:35", "17:20")
    }

def parse_lesson_plan():
    """Parses the lesson plan and returns a list of lesson objects."""
    html = get_html(LESSON_PLAN_URL)
    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. Extract period dates from the header
    header_text = soup.get_text()
    date_range_match = re.search(r"(\d{2}\.\d{2}\.\d{4})\s*-\s*(\d{2}\.\d{2}\.\d{4})", header_text)
    if not date_range_match:
        date_range_match = re.search(r"(\d{2}\.\d{2})\s*-\s*(\d{2}\.\d{2})", header_text)
        if date_range_match:
            year = datetime.now().year
            start_date_str = f"{date_range_match.group(1)}.{year}"
            end_date_str = f"{date_range_match.group(2)}.{year}"
        else:
            raise ValueError("Could not find date range in lesson plan.")
    else:
        start_date_str = date_range_match.group(1)
        end_date_str = date_range_match.group(2)

    start_date = datetime.strptime(start_date_str, "%d.%m.%Y")
    end_date = datetime.strptime(end_date_str, "%d.%m.%Y")
    
    # 2. Find the schedule table
    tables = soup.find_all('table')
    schedule_table = None
    for t in tables:
        if "Esmaspäev" in t.get_text():
            schedule_table = t
            break
            
    if not schedule_table:
        raise ValueError("Could not find schedule table.")

    rows = schedule_table.find_all('tr')
    header_row = rows[0]
    days_raw = [d.get_text(separator=" ", strip=True) for d in header_row.find_all(['td', 'th'], recursive=False)]
    days = days_raw[1:]
    
    lesson_times = parse_timetable_times()
    
    lessons = []
    
    day_map = {
        "Esmaspäev": 0, "Teisipäev": 1, "Kolmapäev": 2, "Neljapäev": 3, "Reede": 4,
        "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4
    }

    for row in rows[1:]:
        cols = row.find_all('td', recursive=False)
        if not cols: continue
        
        lesson_num_text = cols[0].get_text(strip=True)
        try:
            lesson_num = int(lesson_num_text)
        except ValueError:
            continue
            
        time_range = lesson_times.get(lesson_num)
        if not time_range: continue
        start_time_str, end_time_str = time_range
        
        for i, col in enumerate(cols[1:]):
            if i >= len(days): break
            day_idx = -1
            for k, v in day_map.items():
                if k.lower() in days[i].lower():
                    day_idx = v
                    break
            
            if day_idx == -1: continue
            
            # Get all text in the cell, normalized
            all_cell_text = col.get_text(separator="\n", strip=True)
            raw_lines = [line.strip() for line in all_cell_text.split("\n") if line.strip()]
            
            # Group lines into lessons. A new lesson starts if a line starts with a known abbreviation.
            current_lesson_chunks = []
            lesson_blocks = []
            
            known_abbrs = list(LESSON_MAPPINGS.keys())
            
            for line in raw_lines:
                # Does this line look like a new lesson start?
                is_new_lesson = False
                for abbr in sorted(known_abbrs, key=len, reverse=True):
                    # Match abbr followed by space, digit, or end of string
                    if re.match(fr"^{abbr}([\d/]*)(?![a-zA-ZõäöüŠšŽž])", line, re.IGNORECASE):
                        is_new_lesson = True
                        break
                
                if is_new_lesson and current_lesson_chunks:
                    lesson_blocks.append(" ".join(current_lesson_chunks))
                    current_lesson_chunks = []
                
                current_lesson_chunks.append(line)
            
            if current_lesson_chunks:
                lesson_blocks.append(" ".join(current_lesson_chunks))

            for content in lesson_blocks:
                # Apply mappings and filtering
                skip = False
                
                # Check for groups (IK1, IK2, VK1, VK2 etc.)
                for group_prefix in SELECTED_GROUPS:
                    if re.match(fr"^{group_prefix}([\d/]*)(?![a-zA-ZõäöüŠšŽž])", content):
                        nums_match = re.search(fr"^{group_prefix}([\d/]+)", content)
                        if nums_match:
                            groups_str = nums_match.group(1)
                            groups = re.findall(r"\d+", groups_str)
                            if groups:
                                group_nums = [int(n) for n in groups]
                                selected = SELECTED_GROUPS.get(group_prefix)
                                if selected not in group_nums:
                                    skip = True
                                    break
                
                if skip: continue

                # Check for visibility (SHOW_LESSONS)
                for optional_key in SHOW_LESSONS:
                    if not SHOW_LESSONS[optional_key]:
                        # Match only at the start of the block
                        if re.match(fr"^{optional_key}([\d/]*)(?![a-zA-ZõäöüŠšŽž])", content):
                            skip = True
                            break
                
                if skip: continue

                # Check for teacher selection (e.g., KK)
                for pref, teacher in SELECTED_TEACHERS.items():
                    if re.match(fr"^{pref}([\d/]*)(?![a-zA-ZõäöüŠšŽž])", content):
                        if teacher.lower() not in content.lower():
                            skip = True
                            break
                
                if skip: continue

                # FINAL CLEANUP: If the content doesn't start with ANY known abbreviation, 
                # it's likely a dangling piece of information (like just a room name) 
                # that wasn't grouped correctly. We should probably discard it to keep it "clean".
                has_mapping = False
                for abbr in known_abbrs:
                    if re.match(fr"^{abbr}([\d/]*)(?![a-zA-ZõäöüŠšŽž])", content):
                        has_mapping = True
                        break
                
                if not has_mapping:
                    # This filters out "H203" or "HKaasik" if they appear alone.
                    continue

                # Apply mappings for the subject name
                mapped_content = content
                for abbr, full_name in LESSON_MAPPINGS.items():
                    pattern = fr"^{abbr}([\d/]*)(?![a-zA-ZõäöüŠšŽž])"
                    match = re.match(pattern, content)
                    if match:
                        matched_full = match.group(0)
                        mapped_content = content.replace(matched_full, full_name, 1)
                        break

                lessons.append({
                    'content': mapped_content,
                    'day_idx': day_idx,
                    'start_time': start_time_str,
                    'end_time': end_time_str
                })

    # Final deduplication and informative filtering
    # Sort by day, time, and length descending so we check longer strings first
    lessons.sort(key=lambda x: (x['day_idx'], x['start_time'], x['end_time'], len(x['content'])), reverse=True)
    
    unique_lessons = []
    # Use a dictionary to group by slot
    slots = {}
    for l in lessons:
        slot_key = (l['day_idx'], l['start_time'], l['end_time'])
        if slot_key not in slots:
            slots[slot_key] = []
        
        # Check if this content is already represented in the slot
        is_redundant = False
        for existing in slots[slot_key]:
            if l['content'] == existing or l['content'] in existing:
                is_redundant = True
                break
            if existing in l['content']:
                # This shouldn't happen often because we sort by length desc,
                # but if the existing one is a substring of the current one, 
                # replace it.
                slots[slot_key].remove(existing)
                # Continue checking others, but eventually add this one
                pass
        
        if not is_redundant:
            slots[slot_key].append(l['content'])
            unique_lessons.append(l)

    return {
        'start_date': start_date,
        'end_date': end_date,
        'lessons': unique_lessons
    }

if __name__ == "__main__":
    res = parse_lesson_plan()
    print(f"Period: {res['start_date']} to {res['end_date']}")
    print(f"Found {len(res['lessons'])} lessons.")
    for l in res['lessons'][:5]:
        print(l)
