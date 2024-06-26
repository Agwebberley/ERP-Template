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
    urls_path = os.path.join(os.getcwd(), 'ERP-Template/urls.py')
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

def flush_admin():
    # Remove all admin.py files unless they are in INGORDED_APPS
    # Open the settings.py file and get the INGORDED_APPS
    ignored_apps = get_ignored_apps()
    apps_path = os.path.join(os.getcwd())
    apps = os.listdir(apps_path)
    # Remove the admin.py file for each app
    for app in apps:
        if app not in ignored_apps and os.path.exists(os.path.join(apps_path, app, 'admin.py')):
            os.remove(os.path.join(apps_path, app, 'admin.py'))
    print("Admin files flushed successfully")

def flush_forms():
    # Remove all forms.py files unless they are in INGORDED_APPS
    # Open the settings.py file and get the INGORDED_APPS

    ignored_apps = get_ignored_apps()
    # Get all the apps in the project
    apps_path = os.path.join(os.getcwd())
    apps = os.listdir(apps_path)
    # Remove the forms.py file for each app
    for app in apps:
        if app not in ignored_apps and os.path.exists(os.path.join(apps_path, app, 'forms.py')):
            os.remove(os.path.join(apps_path, app, 'forms.py'))
    print("Forms files flushed successfully")

def flush_views():
    # Remove all views.py files unless they are in INGORDED_APPS
    # Open the settings.py file and get the INGORDED_APPS
    settings_path = os.path.join(os.getcwd(), 'ERP-Template/settings.py')

    ignored_apps = get_ignored_apps()
    # Get all the apps in the project
    apps_path = os.path.join(os.getcwd())
    apps = os.listdir(apps_path)
    # Remove the views.py file for each app
    print(ignored_apps)
    for app in apps:
        if app not in ignored_apps and os.path.exists(os.path.join(apps_path, app, 'views.py')):
            os.remove(os.path.join(apps_path, app, 'views.py'))
    print("Views files flushed successfully")

def get_ignored_apps():
    settings_path = os.path.join(os.getcwd(), 'ERP-Template/settings.py')

    if os.path.exists(settings_path):
        with open(settings_path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if 'IGNORED_APPS' in line:
                ignored_apps = line.split('=')[1].strip()
                break
        ignored_apps = ignored_apps[1:-1].replace("'", '').replace(" ", "").split(',')
        return ignored_apps
def flush_all():
    flush_database()
    flush_urls()
    flush_admin()
    flush_forms()
    flush_views()
    print("All files flushed successfully")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python flush.py [database|urls|both]")
    else:
        command = sys.argv[1]
        if command == 'database':
            flush_database()
        elif command == 'urls':
            flush_urls()
        elif command == 'all' or command == "":
            flush_all()
        elif command == 'admin':
            flush_admin()
        elif command == 'forms':
            flush_forms()
        elif command == 'views':
            flush_views()
        else:
            print("Invalid command")