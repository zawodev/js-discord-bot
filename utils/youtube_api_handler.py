import os

import requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re

api_key = os.getenv("YOUTUBE_API_KEY")

def get_channel_id(channel_name):
    print("api key used")
    try:
        youtube = build("youtube", "v3", developerKey=api_key)

        # Sprawdź, czy podany handler to pełny URL kanału
        if re.match(r'^https:\/\/www\.youtube\.com\/channel\/[a-zA-Z0-9_-]+$', channel_name):
            # Pobierz ID kanału z pełnego URL-a
            channel_id = channel_name.split('/')[-1]
            return channel_id
        else:
            # Pobierz ID kanału z nazwy użytkownika
            request = youtube.channels().list(
                part="id",
                forUsername=channel_name,
                maxResults=1
            )
            response = request.execute()
            if 'items' in response and response['items']:
                return response['items'][0]['id']
            else:
                return channel_name
    except HttpError as e:
        print("Wystąpił błąd HTTP:", e)
        return None
    except Exception as e:
        print("Wystąpił nieoczekiwany błąd:", e)
        return None

def get_video_info(channel_input: str) -> dict:
    print("api key used")
    import re
    # Extract channel ID from URL if a URL is provided
    channel_url_pattern = r"https?://www\.youtube\.com/[@]([^/?]+)"
    match = re.search(channel_url_pattern, channel_input)
    if match:
        channel_id = match.group(1)
        # Fetch channel ID using YouTube API if URL format is provided
        base_url = "https://www.googleapis.com/youtube/v3/channels"
        params = {
            "part": "id",
            "forUsername": channel_id,
            "key": api_key
        }
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch channel information: {e}")
            raise ValueError("Failed to fetch channel information.")
        data = response.json()
        items = data.get("items", [])
        if not items:
            raise ValueError("Channel not found.")
        channel_id = items[0]['id']
    else:
        channel_id = channel_input
    # Proceed with fetching the latest video using the channel ID

    base_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "channelId": channel_id,
        "maxResults": 1,
        "order": "date",
        "type": "video",
        "key": api_key
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch video information: {e}")
        raise ValueError("Failed to fetch video information.")
    data = response.json()
    items = data.get("items", [])
    if not items:
        raise ValueError("No videos found.")
    # Returning all video information as requested
    # print(items[0])
    return items[0]

def get_latest_video_info(channel_name):
    return get_video_info(get_channel_id(channel_name))

if __name__ == "__main__":
    video_info = get_latest_video_info("standupmaths")
    print(video_info)
