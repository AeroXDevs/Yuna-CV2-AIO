import os
import json
import sqlite3
import asyncio
import aiosqlite

# List of DB files found in the codebase
DB_FILES = [
    "db/stickymessages.db",
    "db/customrole.db",
    "db/np.db",
    "db/anti.db",
    "db/counting.db",
    "db/giveaways.db",
    "db/ignore.db",
    "db/autoreact.db",
    "db/autoresponder.db",
    "db/invc.db",
    "db/leveling.db",
    "db/media.db",
    "db/block.db",
    "db/notify.db",
    "db/tickets.db",
    "db/badges.db",
    "db/ai_data.db",
    "db/backups.db",
    "db/prefix.db",
    "db/adminlock.db",
    "db/blacklist.db",
    "db/vanity.db",
    "db/nightmode.db",
    "db/welcome.db"
]

# List of JSON files found/typical
JSON_FILES = [
    "config.json",
    "jsondb/noprefix.json",
    "jsondb/extra_owners.json",
    "jsondb/bot_configs.json"
]

def init_files():
    # Ensure directories exist
    for folder in ["db", "jsondb", "logs"]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created directory: {folder}")

    # Initialize SQLite DBs (just create empty file)
    for db_path in DB_FILES:
        if not os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            conn.close()
            print(f"Initialized empty DB: {db_path}")

    # Initialize JSON files (empty dict)
    for json_path in JSON_FILES:
        if not os.path.exists(json_path):
            with open(json_path, 'w') as f:
                json.dump({}, f)
            print(f"Initialized empty JSON: {json_path}")

if __name__ == "__main__":
    init_files()
    print("Database and JSON initialization complete.")
