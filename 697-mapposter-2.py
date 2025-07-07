# 697 robotz
# june 29, 2025
# how to build a bot to automatically post good references for map design

# set up
from dotenv import load_dotenv
import os
from pathlib import Path
import random
import requests
from datetime import datetime

# accessing the tokens
load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")

# getting images
folder_path = Path('/Users/aliceviggiani/Dropbox/1 estudos/5 data viz/0 master/pratt/2.5 2025 summer/697-botz/2-assignments/3 maprobot/img_resized')

image_urls = []

for f in folder_path.iterdir():
    file_name = f.name
    url_gh = f'https://aliceaviggiani.github.io/map-bot/img_resized/{file_name}'
    image_urls.append(url_gh)

# selecting the post content to upload
image_url = random.choice(image_urls)
caption = 'Posted from the Internet Archive metadata by a bot.'


# creating the post content to upload
post_url = f'https://graph.facebook.com/v19.0/{INSTAGRAM_ACCOUNT_ID}/media'

post_content = {
    'image_url': image_url,
    'caption': caption,
    'access_token': ACCESS_TOKEN
}

post_request = requests.post(post_url, data=post_content)

if post_request.status_code != 200:
    print("Error:", post_request.text)
    exit()


# geting the id of the post
post_id = post_request.json().get("id")

url_publish = f"https://graph.facebook.com/v19.0/{INSTAGRAM_ACCOUNT_ID}/media_publish"

publish_wrap = {
    'creation_id': post_id,
    'access_token': ACCESS_TOKEN
}


# publishing!
publish_request = requests.post(url_publish, data=publish_wrap)
if publish_request.status_code != 200:
    print("Error:", publish_request.text)
    exit()

time = datetime.now().strftime("%m/%d/%Y at %H:%M")
print(f'It worked on {time} with the post id: {post_id} :)')