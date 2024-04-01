# There are three commands in this file:
# 1. flush database
# 2. flush urls
# 3 flush both

import os
import sys
import shutil

def flush_database():
    # Define the path to the database file
    db_path = os.path.join(os.getcwd(), 'db.sqlite3')
    # Check if the database file exists
    if os.path.exists(db_path):
        # Remove the database file
        os.remove(db_path)
        print("Database flushed successfully")
    else:
        print("Database file not found")

def flush_urls():
    # remove everything in the main urls.py file after the ']' character
    urls_path = os.path.join(os.getcwd(), '/GlobexCore/urls.py')
    if os.path.exists(urls_path):
        with open(urls_path, 'r') as f:
            lines = f.readlines()
        with open(urls_path, 'w') as f:
            for line in lines:
                if ']' in line:
                    f.write(line)
                    break
                f.write(line)
        print("URLs flushed successfully")
    else:
        print("urls.py file not found")

def flush_both():
    flush_database()
    flush_urls()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python flush.py [database|urls|both]")
    else:
        command = sys.argv[1]
        if command == 'database':
            flush_database()
        elif command == 'urls':
            flush_urls()
        elif command == 'both':
            flush_both()
        else:
            print("Invalid command")