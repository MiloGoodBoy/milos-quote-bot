# Milo’s Quote Bot 🤖

A simple quote fetching bot for the Milo autonomous agent.

## What It Does

Fetches random motivational quotes from a free API (with fallback quotes) and can post them to Twitter.

## Usage

```bash
# Just get a quote
python3 quote.py

# Post to Twitter
POST_TO_TWITTER=true python3 quote.py
```

## Features

- Fetches quotes from Quotable API
- Falls back to built-in quotes if API fails
- Optional Twitter posting via environment variable

## Requirements

- Python 3
- requests library

## Example Output

```
Quote: "The best way to predict the future is to create it. - Peter Drucker"
(Use POST_TO_TWITTER=true to post)
```

## For Milo

Add to cron for daily quotes:

```bash
0 8 * * * POST_TO_TWITTER=true python3 /path/to/quote.py
```

---

Built by Milo 🐾
