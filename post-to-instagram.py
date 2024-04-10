import os
import subprocess
import requests
import json
from instabot import Bot

# Variables

# Directory path containing sub-directories with photos, 
# each sub-directory should also have a file called trip-details.txt that speaks something about the trip
riding_photos_directory = "<local directory path>"
instagram_username = "<mention-instagram-username>"
instagram_password = "<mention-instagram-password>"
# TODO: Different trending song for each instagram post
trending_song = ""
api_key = "<OpenAI API token>"  

# Function to generate Instagram caption using OpenAI GPT API
def generate_caption(summary):
    response = requests.post(
        "https://api.openai.com/v1/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(api_key)
        },
        json={
            "model": "gpt-3.5-turbo-instruct",
            "prompt":"Write an instagram post caption for the following summary of a superbikes ride group in 100-200 words. Also include relevant trending hastags. Summary is:" + summary,
            "max_tokens": 200
        }
    )
    response_json = response.json()
    caption = response_json["choices"][0]["text"]
    return caption

# Navigate to the Riding-Photos directory
os.chdir(riding_photos_directory)

# Loop through each sub-directory
for dir in os.listdir():
    if not os.path.isdir(dir):
        continue
    
    os.chdir(os.path.join(riding_photos_directory, dir))  # Enter the sub-directory
    
    # Select the first four photos in incremental order of timestamps
    photos = sorted(filter(lambda x: x.endswith('.jpg'), os.listdir()), key=os.path.getmtime)[:4]

    # Read the trip-details.txt file for caption content
    with open('trip-details.txt', 'r') as file:
        extracted_caption = file.read()

    # Generate a caption using OpenAI GPT API
    final_caption = generate_caption(extracted_caption)

    # Combine trip details, random caption, and the name of the trending song
    caption_to_post = "{} Tagging: {}".format(final_caption, trending_song)

    print(caption_to_post)
    
    # Instantiate Instabot
    bot = Bot()

    # Logout from Instagram
    bot.logout()
 
    # Login to Instagram
    bot.login(username=instagram_username, password=instagram_password)
    
    # Upload photos with caption
    print("Total number of photos: {}".format(len(photos)))
    for photo in photos:
        bot.upload_photo(photo, caption=caption_to_post)
        print("Uploaded")
    
    # Logout from Instagram
    bot.logout()
    
    # Navigate back to the parent directory
    os.chdir(riding_photos_directory)
