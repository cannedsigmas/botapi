import requests
import random
import string
import json
import os
import time
import threading

# Change this if you're running in Railway or GitHub Actions
output_dir = r"C:\Users\canne\OneDrive\Documents\usernamedatabase"
os.makedirs(output_dir, exist_ok=True)

file_path = os.path.join(output_dir, 'usernames_passwords.json')

def generate_random_username(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def generate_random_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def is_username_valid_and_available(username):
    url = "https://users.roblox.com/v1/usernames/users"
    payload = {
        "usernames": [username],
        "excludeBannedUsers": False
    }
    try:
        res = requests.post(url, json=payload)
        res.raise_for_status()
        data = res.json()
        return not data.get("data")  # True if username is available
    except Exception as e:
        print(f"Error checking {username}: {e}")
        return False

def save_to_json(username, password, file_path):
    new_entry = {'username': username, 'password': password}
    
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as f:
            existing_data = json.load(f)
    else:
        existing_data = []
    
    existing_data.append(new_entry)

    with open(file_path, 'w') as f:
        json.dump(existing_data, f, indent=4)
    
    print(f"✅ Saved {username} to {file_path}")

def remove_from_json(username, file_path):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as f:
            existing_data = json.load(f)
        
        updated_data = [entry for entry in existing_data if entry['username'] != username]

        with open(file_path, 'w') as f:
            json.dump(updated_data, f, indent=4)

        print(f"❌ Removed {username} from {file_path}")
    else:
        print("JSON file not found or empty.")

def generate_and_check_usernames():
    def check_username(username):
        if is_username_valid_and_available(username):
            password = generate_random_password()
            save_to_json(username, password, file_path)
        else:
            print(f"❌ Username {username} is taken.")

    while True:
        username = generate_random_username()
        threading.Thread(target=check_username, args=(username,)).start()
        time.sleep(1)

if __name__ == "__main__":
    generate_and_check_usernames()
