"""
Publish Helper Script

This script helps you manage your personal data when switching between
"work" mode (using your personal calendar) and "publish" mode (sharing on GitHub).

Usage:
    python publish_helper.py backup   - Save personal data to my_personal_data.json
    python publish_helper.py restore  - Restore personal data from my_personal_data.json
"""

import json
import os
import sys
import shutil

BACKUP_FILE = "my_personal_data.json"

# Files to back up
SENSITIVE_FILES = ["token.json", "credentials.json"]

# Config values to back up (these are the personal settings in config.py)
CONFIG_FILE = "config.py"


def read_config_values():
    """Read the current config.py and extract personal values."""
    config_data = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            # We'll store the entire config content for simplicity
            config_data['config_content'] = content
    return config_data


def backup():
    """Backup all personal data to a single JSON file."""
    print("Backing up personal data...")
    
    backup_data = {
        'files': {},
        'config': {}
    }
    
    # Backup sensitive files
    for filename in SENSITIVE_FILES:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                try:
                    backup_data['files'][filename] = json.load(f)
                    print(f"  Backed up: {filename}")
                except json.JSONDecodeError:
                    backup_data['files'][filename] = f.read()
                    print(f"  Backed up (as text): {filename}")
        else:
            print(f"  Skipped (not found): {filename}")
    
    # Backup config.py content
    config_values = read_config_values()
    if config_values:
        backup_data['config'] = config_values
        print(f"  Backed up: {CONFIG_FILE}")
    
    # Write the backup file
    with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nBackup complete! Your personal data is saved in: {BACKUP_FILE}")
    print("You can now move this file out of the project folder before publishing.")
    print("\nTo prepare for publishing, you can delete the sensitive files:")
    for filename in SENSITIVE_FILES:
        if os.path.exists(filename):
            print(f"  - {filename}")


def restore():
    """Restore personal data from the backup JSON file."""
    if not os.path.exists(BACKUP_FILE):
        print(f"Error: Backup file '{BACKUP_FILE}' not found.")
        print("Make sure you have moved it back into the project folder.")
        return
    
    print("Restoring personal data...")
    
    with open(BACKUP_FILE, 'r', encoding='utf-8') as f:
        backup_data = json.load(f)
    
    # Restore sensitive files
    for filename, content in backup_data.get('files', {}).items():
        with open(filename, 'w', encoding='utf-8') as f:
            if isinstance(content, dict):
                json.dump(content, f, indent=2, ensure_ascii=False)
            else:
                f.write(content)
        print(f"  Restored: {filename}")
    
    # Restore config.py
    config_data = backup_data.get('config', {})
    if 'config_content' in config_data:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            f.write(config_data['config_content'])
        print(f"  Restored: {CONFIG_FILE}")
    
    print("\nRestore complete! Your personal settings are back.")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("Commands:")
        print("  backup  - Save your personal data before publishing")
        print("  restore - Restore your personal data after publishing")
        return
    
    command = sys.argv[1].lower()
    
    if command == "backup":
        backup()
    elif command == "restore":
        restore()
    else:
        print(f"Unknown command: {command}")
        print("Use 'backup' or 'restore'.")


if __name__ == "__main__":
    main()
