#!/usr/bin/env python3
"""
Wealth Insights Global Autoposter
Posts to Wealth Insights Global Facebook page — 24 posts per day, one every hour.
Covers all topics: Personal Finance, Money Management, Wealth, Side Hustles, Online Income.
Triggered by GitHub Actions cron schedule.
"""

import os
import json
import requests
from datetime import datetime


# ── Config ────────────────────────────────────────────────────────────────────
PAGE_ACCESS_TOKEN = os.environ.get("FACEBOOK_PAGE_ACCESS_TOKEN")
PAGE_ID           = "985495971313538"  # Wealth Insights Global Facebook Page
POSTS_FILE        = os.path.join(os.path.dirname(__file__), "posts.json")


# ── Helpers ───────────────────────────────────────────────────────────────────
def get_current_hour() -> int:
    return datetime.utcnow().hour


def load_posts(filepath: str) -> list:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def get_post_for_hour(posts: list, hour: int) -> dict | None:
    for post in posts:
        if post.get("hour") == hour:
            return post
    return None


def publish_to_facebook(page_id: str, token: str, message: str) -> dict:
    url     = f"https://graph.facebook.com/v19.0/{page_id}/feed"
    payload = {"message": message, "access_token": token}
    resp    = requests.post(url, data=payload, timeout=30)
    return resp.json()


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    if not PAGE_ACCESS_TOKEN:
        raise EnvironmentError("Missing secret: FACEBOOK_PAGE_ACCESS_TOKEN")

    posts = load_posts(POSTS_FILE)
    hour  = get_current_hour()

    print(f"[{datetime.utcnow().isoformat()}] Wealth Insights Global Autoposter — UTC hour: {hour}")

    post = get_post_for_hour(posts, hour)

    if not post:
        print(f"No post scheduled for hour {hour}. Skipping.")
        return

    print(f"Publishing post ID {post['id']} (hour {hour})...")
    print(f"Preview: {post['content'][:100]}...")

    result = publish_to_facebook(PAGE_ID, PAGE_ACCESS_TOKEN, post["content"])

    if "id" in result:
        print(f"SUCCESS — Post published. Facebook ID: {result['id']}")
    else:
        print(f"FAILED — API response: {result}")
        raise RuntimeError(f"Facebook API error: {result}")


if __name__ == "__main__":
    main()
