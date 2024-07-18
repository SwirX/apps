import json
import os
import shutil
import subprocess
from github import Github
from dotenv import load_dotenv

load_dotenv()

# Configuration
USERNAME = "SwirX"
REPO_NAME = "apps"
REPO_PATH = os.getenv("REPO_PATH")
APPS_JSON_PATH = os.path.join(REPO_PATH, 'applist.json')
GITHUB_REPO_URL = f'git@github.com:{USERNAME}/{REPO_NAME}.git'
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Create a token at https://github.com/settings/tokens

# Initialize GitHub API client
g = Github(GITHUB_TOKEN)
repo = g.get_repo(f"{USERNAME}/{REPO_NAME}")

def add_app():
    app_name = input("Enter the app name: ")
    files = []

    while True:
        file_path = input("Enter the file path (or 'c'/'continue' to finish): ").strip()
        if file_path.lower() in ['c', 'continue']:
            break
        if os.path.exists(file_path):
            files.append(file_path)
        else:
            print(f"File {file_path} does not exist. Please enter a valid path.")

    # Update JSON file
    if os.path.exists(APPS_JSON_PATH):
        with open(APPS_JSON_PATH, 'r') as f:
            apps_data = json.load(f)
    else:
        apps_data = {}

    if app_name not in apps_data:
        apps_data[app_name] = []

    for file_path in files:
        file_name = os.path.basename(file_path)
        apps_data[app_name].append(file_name)

        # Copy file to the appropriate directory
        dest_dir = os.path.join(REPO_PATH, 'apps', app_name)
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copy(file_path, os.path.join(dest_dir, file_name))

    with open(APPS_JSON_PATH, 'w') as f:
        json.dump(apps_data, f, indent=4)

def git_commit_and_push():
    # Change directory to the local repo path
    os.chdir(REPO_PATH)
    
    # Git add, commit and push
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', 'Update apps and JSON file'])
    subprocess.run(['git', 'push', 'origin', 'main'])

def main():
    add_app()
    git_commit_and_push()
    print("App added and changes pushed to GitHub.")

if __name__ == "__main__":
    main()
