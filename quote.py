#!/usr/bin/env python3
"""
Milo's Quote Bot
Fetches random quotes and posts to Twitter/Moltbook
"""
import requests
import random
import os
import json

QUOTE_API = "https://api.quotable.io/random"

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
    quote = get_quote()
    print(f"Quote: {quote}")
    
    # Post to Twitter if enabled
    if os.environ.get("POST_TO_TWITTER", "false").lower() == "true":
        if post_twitter(quote):
            print("✅ Posted to Twitter")
        else:
            print("❌ Failed to post to Twitter")
    else:
        print("(Use POST_TO_TWITTER=true to post)")
