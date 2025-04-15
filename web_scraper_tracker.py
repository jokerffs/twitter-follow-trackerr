import requests
from bs4 import BeautifulSoup
import time
import telegram

# Telegram bot setup
bot_token = "7788051366:AAEGYsJY1JdF8-unUxSGslNll1G3BOOgOds"  # Your bot token
chat_id = "977248982"  # Your chat ID
bot = telegram.Bot(token=bot_token)

# Target Twitter usernames
usernames = ["Gautamguptagg", "reverse3406"]  # Added @reverse3406
url_template = "https://twitter.com/{}/following"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Previous followings for each user
prev_followings = {username: set() for username in usernames}

def send_telegram_message(message):
    bot.send_message(chat_id=chat_id, text=message)

def fetch_followings(username):
    try:
        url = url_template.format(username)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Scrape users from profile (limited and not always reliable)
        users = set()
        for tag in soup.find_all("a"):
            href = tag.get("href", "")
            if href.startswith("/") and href.count("/") == 1 and href.strip("/") != username:
                users.add(href.strip("/"))
        return users
    except Exception as e:
        print(f"[Error] {e}")
        return set()

# Start tracking
print("Tracking follows for users: @Gautamguptagg, @reverse3406...\n")

# Initialize previous followings
for username in usernames:
    prev_followings[username] = fetch_followings(username)

while True:
    time.sleep(60)  # Check every 1 minute

    for username in usernames:
        current_followings = fetch_followings(username)
        new_follows = current_followings - prev_followings[username]

        if new_follows:
            for user in new_follows:
                message = f"🟢 @{username} followed: @{user}"
                print(message)
                send_telegram_message(message)
        else:
            print(f"No new follows for @{username}...")

        prev_followings[username] = current_followings
