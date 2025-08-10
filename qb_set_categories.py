#!/usr/bin/env python3
"""
Automatically set the categories for torrents with known file extensions.
"""

import requests
import time

QBT_HOST = "http://127.0.0.1:8990"
USERNAME = "admin"
TARGET_CATEGORY = "musique"

session = requests.Session()

# Ordered dictionary.
EXT_TO_CATEGORY = {"musique": {"mp3", "flac", "wav"}, "nas": {"mp4", "mkv"}}


def login():
    url = f"{QBT_HOST}/api/v2/auth/login"
    resp = session.post(
        url,
        data={"username": USERNAME},
    )
    resp.raise_for_status()
    if resp.text != "Ok.":
        raise Exception("Login failed")


def get_torrents():
    url = f"{QBT_HOST}/api/v2/torrents/info"
    resp = session.get(url)
    resp.raise_for_status()
    return resp.json()


def get_categories():
    url = f"{QBT_HOST}/api/v2/torrents/categories"
    resp = session.get(url)
    resp.raise_for_status()
    return resp.json()


def get_files(torrent_hash):
    url = f"{QBT_HOST}/api/v2/torrents/files?hash={torrent_hash}"
    resp = session.get(url)
    resp.raise_for_status()
    return resp.json()


def set_category(torrent_hash, category):
    url = f"{QBT_HOST}/api/v2/torrents/setCategory"
    resp = session.post(url, data={"hashes": torrent_hash, "category": category})
    resp.raise_for_status()
    return resp.text == "Ok."


def main():
    login()

    categories = get_categories()
    for category in EXT_TO_CATEGORY.keys():
        if category not in categories:
            print(f"Category '{category}' does not exist. Exiting.")
            return

    torrents = get_torrents()
    seven_days_ago = time.time() - 7 * 24 * 3600

    for t in torrents:
        added_on = t.get("added_on")
        if not added_on or added_on < seven_days_ago:
            continue

        # Only process torrents without a category
        if t.get("category"):
            continue

        files = get_files(t["hash"])
        extensions = {f["name"].lower().split(".")[-1] for f in files}
        for cat, exts in EXT_TO_CATEGORY.items():
            if extensions & exts:
                print(f"Setting category to '{cat}' for torrent '{t['name']}'")
                set_category(t["hash"], cat)
                break


if __name__ == "__main__":
    main()
