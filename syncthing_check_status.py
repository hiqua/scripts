#!/usr/bin/env python3
import requests
import json
import os
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SYNCTHING_API_KEY = os.getenv("SYNCTHING_API_KEY")
if not SYNCTHING_API_KEY:
    logging.error("SYNCTHING_API_KEY environment variable not set.")
    exit(1)

SYNCTHING_ADDRESS = "http://localhost:8384"

def get_folder_ids():
    """Gets a list of all folder IDs."""
    try:
        headers = {"X-API-Key": SYNCTHING_API_KEY}
        response = requests.get(f"{SYNCTHING_ADDRESS}/rest/stats/folder", headers=headers)
        response.raise_for_status()
        return list(response.json().keys())
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while getting folder IDs: {e}")
        return []
    except json.JSONDecodeError:
        logging.error("Could not decode JSON response from Syncthing API when getting folder IDs.")
        return []

def check_device_synced(device_id):
    """
    Checks if a specific device is fully synced with the local Syncthing instance.
    """
    try:
        headers = {"X-API-Key": SYNCTHING_API_KEY}

        response = requests.get(f"{SYNCTHING_ADDRESS}/rest/system/connections", headers=headers)
        response.raise_for_status()
        connections = response.json()

        if device_id not in connections.get("connections", {}):
             logging.warning(f"Device {device_id} is not connected.")
             return

        device_connection = connections["connections"][device_id]
        logging.info(f"Device {device_id} is connected: {device_connection.get('connected', False)}")
        if not device_connection.get('connected', False):
            return


        folder_ids = get_folder_ids()
        if not folder_ids:
            logging.error("Could not retrieve folder list. Exiting.")
            return

        all_synced = True
        for folder_id in folder_ids:
            response = requests.get(f"{SYNCTHING_ADDRESS}/rest/db/completion?device={device_id}&folder={folder_id}", headers=headers)
            response.raise_for_status()
            completion_data = response.json()

            completion_percent = completion_data.get("completion", 0)

            if completion_percent != 100:
                all_synced = False
                logging.warning(f"Device {device_id} is not fully synced for folder '{folder_id}'. Completion: {completion_percent}%")
                needed_bytes = completion_data.get("needBytes", 0)
                logging.info(f"  {needed_bytes} bytes remaining to sync.")

        if all_synced:
            logging.info(f"Device {device_id} is fully synced for all folders.")


    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred: {e}")
    except json.JSONDecodeError:
        logging.error("Could not decode JSON response from Syncthing API.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check if a Syncthing device is fully synced.")
    parser.add_argument("device_id", help="The ID of the device to check.")
    args = parser.parse_args()
    check_device_synced(args.device_id)
