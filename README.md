# TikTok Data Analysis Project

This project provides a Python script for analyzing a user's TikTok data, focusing on aspects such as watch sessions, comments, likes, shares, live streams, and login history. The script reads data from a JSON file and computes various metrics to offer insights into the user's interaction with the TikTok platform.

## Dependencies

- Python 3.x
- NumPy
- Emoji
- Regular Expressions (re module)

## Installation

Ensure you have Python installed on your system. The script requires the `numpy` and `emoji` libraries, which can be installed using pip:

pip install numpy emoji

## Usage

Place the TikTok data file (`user_data.json`) in a directory and update the `file_path` variable in the script to point to its location. Run the script to perform the analysis. The script will output the analysis results for each category.

## Features

The script analyzes the following aspects of TikTok data:

1. **Watch Sessions**:
   - Total videos watched
   - Total watch time in minutes
   - Number of watch sessions
   - Average session length in minutes
   - Longest watch session in minutes
   - Earliest and latest video watched
   - Most active weekday

2. **Comments**:
   - Total number of comments
   - Average comment length
   - Most used emoji and its count

3. **Likes**:
   - Total likes
   - Day with most liked posts and the count
   - First liked video
   - First liked video date

4. **Shares**:
   - Total shares
   - Day with most shared posts and the count
   - First shared video
   - First shared video date

5. **Live Streams**:
   - Total lives viewed
   - Earliest and latest watched live stream

6. **Login History**:
   - Times logged in
   - Most used device model
   - Most used network type
   - Most used carrier

## Data Privacy

Ensure that you have the right to access and analyze the data. The script is intended for personal use and analysis only.

## License

This project is free to use and modify for personal purposes.