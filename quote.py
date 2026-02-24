#!/usr/bin/env python3
"""
Milo's Quote Bot
Fetches random quotes and posts to Twitter/Moltbook
Stores quote history for tracking favorites
"""
import requests
import random
import os
import json
from datetime import datetime

QUOTE_API = "https://api.quotable.io/random"
HISTORY_FILE = os.path.expanduser("~/.milo-quote-history.json")

FALLBACK_QUOTES = [
    "The best way to predict the future is to create it. - Peter Drucker",
    "Innovation distinguishes between a leader and a follower. - Steve Jobs",
    "Stay hungry, stay foolish. - Steve Jobs",
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Life is what happens when you're busy making other plans. - John Lennon",
    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
    "It does not matter how slowly you go as long as you do not stop. - Confucius",
    "Everything you've ever wanted is on the other side of fear. - George Addair",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
    "The best time to plant a tree was 20 years ago. The second best time is now. - Chinese Proverb",
]

def load_history():
    """Load quote history from file"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return []

def save_history(history):
    """Save quote history to file"""
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def add_to_history(quote):
    """Add a quote to history"""
    history = load_history()
    history.append({
        "quote": quote,
        "timestamp": datetime.now().isoformat()
    })
    # Keep last 100 quotes
    history = history[-100:]
    save_history(history)

def show_history(count=10):
    """Show recent quotes"""
    history = load_history()
    if not history:
        print("No quote history yet!")
        return
    print(f"Recent {count} quotes:")
    for i, entry in enumerate(history[-count:], 1):
        print(f"{i}. {entry['quote']}")
        print(f"   {entry['timestamp'][:10]}\n")

def get_quote():
    """Fetch a random quote"""
    try:
        response = requests.get(QUOTE_API, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return f'"{data["content"]}" - {data["author"]}'
    except:
        pass
    return random.choice(FALLBACK_QUOTES)

def post_twitter(quote):
    """Post to Twitter"""
    try:
        import subprocess
        cmd = f'''node -e "
const {{TwitterApi}} = require('twitter-api-v2');
const fs = require('fs');
const creds = JSON.parse(fs.readFileSync('/home/ubuntu/.openclaw/config/twitter-credentials.json'));
const client = new TwitterApi({{appKey: creds.api_key, appSecret: creds.api_secret, accessToken: creds.access_token, accessSecret: creds.access_token_secret}});
client.v2.tweet(\`{quote}\`).then(r=>console.log('OK')).catch(e=>console.error(e));"
'''
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
        return result.returncode == 0
    except Exception as e:
        print(f"Twitter error: {e}")
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Milo's Quote Bot")
    parser.add_argument("--history", "-H", action="store_true", help="Show quote history")
    parser.add_argument("--count", "-c", type=int, default=10, help="Number of history items to show")
    args = parser.parse_args()
    
    if args.history:
        show_history(args.count)
        exit(0)
    
    quote = get_quote()
    print(f"Quote: {quote}")
    
    # Add to history
    add_to_history(quote)
    
    # Post to Twitter if enabled
    if os.environ.get("POST_TO_TWITTER", "false").lower() == "true":
        if post_twitter(quote):
            print("✅ Posted to Twitter")
        else:
            print("❌ Failed to post to Twitter")
    else:
        print("(Use POST_TO_TWITTER=true to post)")
