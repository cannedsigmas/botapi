import requests
import random
import string
import json
import os
import time
import threading

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
    res = requests.post(url, json=payload)
    data = res.json()

    if data.get("data"):
        return False
    return True

def save_to_json(username, password, file_path):
    data = {'username': username, 'password': password}
    
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as f:
            existing_data = json.load(f)
    else:
        existing_data = []
    
    existing_data.append(data)
    
    with open(file_path, 'w') as f:
        json.dump(existing_data, f, indent=4)
    print(f"Saved {username} with password to {file_path}")

def remove_from_json(username, file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            existing_data = json.load(f)
        
        existing_data = [entry for entry in existing_data if entry['username'] != username]
        
        with open(file_path, 'w') as f:
            json.dump(existing_data, f, indent=4)
        print(f"Removed {username} from {file_path}")

def generate_and_check_usernames():
    def check_username(username):
        if is_username_valid_and_available(username):
            password = generate_random_password()
            save_to_json(username, password, file_path)
        else:
            print(f"Username {username} is taken.")

    while True:
        username = generate_random_username()

        threading.Thread(target=check_username, args=(username,)).start()

        time.sleep(1)

generate_and_check_usernames()
