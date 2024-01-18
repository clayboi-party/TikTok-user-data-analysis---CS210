#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import emoji
import re
import numpy as np
from datetime import datetime, timedelta
from collections import Counter

# Load the JSON data from the uploaded file
file_path = r'C:\Users\sarp2\Desktop\user_data.json'

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        tiktok_data = json.load(file)
    message = "JSON data loaded successfully."
except Exception as e:
    tiktok_data = None
    message = f"Error loading JSON data: {e}"

print(message)



def analyze_watch_sessions(data):
    # Extracting the "VideoList" from the data
    video_history = data.get("Activity", {}).get("Video Browsing History", {}).get("VideoList", [])
    
    # Total videos watched
    total_videos_watched = len(video_history)

    # Converting dates to datetime objects
    watch_dates = [datetime.strptime(video["Date"], "%Y-%m-%d %H:%M:%S") for video in video_history]

    # Earliest and latest video watched
    earliest_video = min(watch_dates).strftime("%Y-%m-%d %H:%M:%S") if watch_dates else None
    latest_video = max(watch_dates).strftime("%Y-%m-%d %H:%M:%S") if watch_dates else None

    # Determining session lengths and most active weekday
    watch_dates.sort()
    session_lengths = []
    session_start = watch_dates[0]
    for i in range(1, len(watch_dates)):
        if (watch_dates[i] - watch_dates[i - 1]) > timedelta(hours=1):  # Assuming a new session starts after an hour gap
            session_lengths.append((watch_dates[i - 1] - session_start).total_seconds() / 60)  # Convert to minutes
            session_start = watch_dates[i]
    session_lengths.append((watch_dates[-1] - session_start).total_seconds() / 60)  # Convert to minutes

    # Total watch time in minutes
    total_watch_time = sum(session_lengths)

    # Average session length in minutes
    avg_session_length = np.mean(session_lengths) if session_lengths else 0

    # Longest watch session in minutes
    longest_watch_session = max(session_lengths) if session_lengths else 0

    # Most active weekday
    weekdays = [d.strftime("%A") for d in watch_dates]
    most_active_weekday = max(set(weekdays), key=weekdays.count)

    return {
        "Total videos watched": total_videos_watched,
        "Total watch time (minutes)": total_watch_time,
        "Watch sessions": len(session_lengths),
        "Average session length (minutes)": avg_session_length,
        "Longest watch session (minutes)": longest_watch_session,
        "Earliest video watched": earliest_video,
        "Last video watched": latest_video,
        "Most active weekday": most_active_weekday
    }

# To extract emojis
def get_emojis(text):
    # Regular expression to match all emojis
    emoji_pattern = re.compile("[" 
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251" 
                               "]+", flags=re.UNICODE)
    return emoji_pattern.findall(text)

def analyze_comments(data):
    # Extracting the "CommentsList" from the data
    comments_data = data.get("Comment", {}).get("Comments", {}).get("CommentsList", [])
    
    # Total comments
    total_comments = len(comments_data)

    # Average comment length
    avg_comment_length = sum(len(comment["Comment"]) for comment in comments_data) / total_comments if comments_data else 0

    # Most used emoji and its count
    all_emojis = ''.join(emoji for comment in comments_data for emoji in get_emojis(comment["Comment"]))
    emoji_count = Counter(all_emojis)
    most_used_emoji, most_used_emoji_count = emoji_count.most_common(1)[0] if emoji_count else (None, 0)

    return {
        "Total Comments": total_comments,
        "Average Comment Length": avg_comment_length,
        "Most used emoji": most_used_emoji,
        "Most used emoji count": most_used_emoji_count
    }

def analyze_likes(data):
    activity_data = data.get("Activity", {})
    liked_videos = activity_data.get("Like List", {}).get("ItemFavoriteList", [])
    
    # Total likes
    total_likes = len(liked_videos)

    # Day with most liked posts and the count
    like_dates = [datetime.strptime(item["Date"], "%Y-%m-%d %H:%M:%S").date() for item in liked_videos]
    most_liked_day, most_liked_count = Counter(like_dates).most_common(1)[0] if like_dates else (None, 0)

    # First liked video and its date
    if liked_videos:
        first_liked_video = liked_videos[-1]["Link"]
        first_liked_video_date = datetime.strptime(liked_videos[-1]["Date"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
    else:
        first_liked_video = None
        first_liked_video_date = None

    return {
        "Total likes": total_likes,
        "Day with most liked posts": str(most_liked_day),
        "Likes count on that day": most_liked_count,
        "First liked video": first_liked_video,
        "Date of first liked video": first_liked_video_date
    }

def analyze_shares(data):
    # Extracting the "ShareHistoryList" from the data
    shared_videos = data.get("Activity", {}).get("Share History", {}).get("ShareHistoryList", [])
    
    # Total shares
    total_shares = len(shared_videos)

    # Day with most shared posts and the count
    share_dates = [datetime.strptime(item["Date"], "%Y-%m-%d %H:%M:%S").date() for item in shared_videos]
    most_shared_day, most_shared_count = Counter(share_dates).most_common(1)[0] if share_dates else (None, 0)

    # First shared video
    first_shared_video = shared_videos[-1]["Link"] if shared_videos else None

    return {
        "Total shares": total_shares,
        "Day with most shared posts": str(most_shared_day),
        "Shares count on that day": most_shared_count,
        "First shared video": first_shared_video
    }

def analyze_live_streams(data):
    # Adjusting to the structure where "Tiktok Live" is directly under the main data
    tiktok_live_data = data.get("Tiktok Live", {}).get("Watch Live History", {}).get("WatchLiveMap", {})
    
    # Total Lives viewed
    total_lives_viewed = len(tiktok_live_data)

    # Extracting individual watch times and links
    watch_times = [datetime.strptime(live["WatchTime"], "%Y-%m-%d %H:%M:%S") for live in tiktok_live_data.values()]
    watch_links = [live["Link"] for live in tiktok_live_data.values()]

    # Sorting by watch time to get the earliest and latest
    sorted_watch_times = sorted(watch_times)
    earliest_watch_time = sorted_watch_times[0] if watch_times else None
    latest_watch_time = sorted_watch_times[-1] if watch_times else None
    earliest_watch_link = watch_links[watch_times.index(earliest_watch_time)] if earliest_watch_time else None
    latest_watch_link = watch_links[watch_times.index(latest_watch_time)] if latest_watch_time else None

    return {
        "Total Lives viewed": total_lives_viewed,
        "Earliest watched live": {
            "Date": str(earliest_watch_time),
            "Link": earliest_watch_link
        },
        "Latest watched live": {
            "Date": str(latest_watch_time),
            "Link": latest_watch_link
        }
    }

def analyze_login_history(data):
    # Extracting the "LoginHistoryList" from the data
    login_history = data.get("Activity", {}).get("Login History", {}).get("LoginHistoryList", [])
    
    # Total times logged in
    total_logins = len(login_history)

    # Most used device model
    device_models = [login["DeviceModel"] for login in login_history]
    most_used_device_model = max(set(device_models), key=device_models.count) if device_models else None

    # Most used network type
    network_types = [login["NetworkType"] for login in login_history]
    most_used_network_type = max(set(network_types), key=network_types.count) if network_types else None

    # Most used carrier
    carriers = [login["Carrier"] for login in login_history]
    most_used_carrier = max(set(carriers), key=carriers.count) if carriers else None

    return {
        "Times Logged In": total_logins,
        "Most Used Device Model": most_used_device_model,
        "Most Used Network Type": most_used_network_type,
        "Most Used Carrier": most_used_carrier
    }

# To use these functions
watch_session_analysis = analyze_watch_sessions(tiktok_data)
comments_analysis = analyze_comments(tiktok_data)
likes_analysis = analyze_likes(tiktok_data)
shares_analysis = analyze_shares(tiktok_data)
live_streams_analysis = analyze_live_streams(tiktok_data)
login_analysis = analyze_login_history(tiktok_data)

# Displaying the results
watch_session_analysis, comments_analysis, likes_analysis, shares_analysis, live_streams_analysis, login_analysis

# In[ ]:



