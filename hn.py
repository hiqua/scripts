#!/usr/bin/env python3
import requests
from datetime import datetime, timedelta, timezone, date
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any


logging.basicConfig(
    level=logging.WARN, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

BASE_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"
TOPSTORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_COMMENT_URL = "https://news.ycombinator.com/item?id={}"

session = requests.Session()


def get_item(item_id: int) -> dict[str, Any] | None:
    url = BASE_ITEM_URL.format(item_id)
    try:
        response = session.get(url)
        response.raise_for_status()
        logger.debug(f"Fetched item {item_id}")
        return response.json()
    except requests.RequestException as e:
        logger.warning(f"Failed to fetch item {item_id}: {e}")
        return None


def get_topstories_ids() -> list[int]:
    try:
        logger.debug("Fetching topstories IDs")
        response = session.get(TOPSTORIES_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch topstories: {e}")
        return []


def timestamp_to_utc_date(ts: int) -> date:
    return datetime.fromtimestamp(ts, timezone.utc).date()


def timestamp_to_local_date(ts: int) -> date:
    """Convert a unix timestamp to the user's local date."""
    return datetime.fromtimestamp(ts).date()


def get_topstories_items(
    max_items: int = 100, max_workers: int = 10
) -> list[dict[str, Any]]:
    ids = get_topstories_ids()[:max_items]
    items: list[dict[str, Any]] = []

    def fetch(id_: int) -> dict[str, Any] | None:
        item = get_item(id_)
        return item if item and item.get("type") == "story" and "time" in item else None

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(fetch, id_) for id_ in ids]
        for future in as_completed(futures):
            item = future.result()
            if item:
                items.append(item)

    logger.info(f"Fetched {len(items)} topstory items concurrently")
    return items


def group_by_day(
    items: list[dict[str, Any]], target_date: date
) -> list[dict[str, Any]]:
    filtered = [
        item for item in items if timestamp_to_local_date(item["time"]) == target_date
    ]
    logger.debug(f"Found {len(filtered)} stories for {target_date}")
    return sorted(filtered, key=lambda x: x.get("score", 0), reverse=True)[:20]


def format_output(items: list[dict[str, Any]], show_title: bool = False) -> list[str]:
    result = []
    for item in items:
        s = HN_COMMENT_URL.format(item["id"])
        if show_title:
            s += f" {item['title']}"
        result.append(s)
    return result


def main(show_title: bool = True, num_days: int = 4) -> dict[int, list[dict[str, Any]]]:
    all_items = get_topstories_items(max_items=5000)

    all_daily_top = {}
    for days_ago in range(num_days):
        target_date = datetime.now().date() - timedelta(days=days_ago)
        daily_top = group_by_day(all_items, target_date)
        print(f"Top {len(daily_top)} topstories for {target_date}:")
        for link in format_output(daily_top, show_title=show_title):
            print(f"{link}")
        if days_ago < num_days - 1:
            print()
        all_daily_top[days_ago] = daily_top
    return all_daily_top


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Show top Hacker News stories by local day."
    )
    parser.add_argument(
        "--no-title",
        action="store_false",
        dest="show_title",
        help="Do not print the story title after the link",
    )
    args = parser.parse_args()
    all_daily_top = main(show_title=args.show_title)
