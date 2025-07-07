# 697 Botz  
July 6, 2025  
Alice Viggiani

A bot to daily post good references for map design from the Internet Archive metadata on Instagram  
Check out the bot: https://www.instagram.com/undr.constrctn

## Tutorial

To build a bot that automatically posts once a day on Instagram, using Internet Archive metadata as a source, and programming with Python on an iMac, it will need to:

1. Set up a Meta Developer environment and accounts as specified, and fulfill other necessary requirements.
2. Write a script to automate an Instagram post using the Meta Graph API.
3. Write a configuration in a .plist file to schedule a trigger that runs the script and save it in the LaunchAgents folder on a Mac computer.
4. Write a script to download a set of images from an Internet Archive search using their API, in accordance with Instagram's requirements.
5. Upload and publish the resulting images in a GitHub repository.
6. Update the first script with the actual images.
7. Repeat steps 4 to 6 when new images are needed.

This tutorial focuses on steps 1 to 3.

## 1. Set up a Meta for Developers environment


### 1.1 From a mobile, create the following accounts:
Instagram Business (you can choose the option "business" while creating), Facebook (doesn't need to be business), and a Facebook page.  
Connect all of them in Facebook > settings > linked accounts

### 1.2 Create a Meta Developer account: 
https://business.facebook.com/business/loginpage/?next=https%3A%2F%2Fdevelopers.facebook.com%2Fasync%2Fregistration#  
Follow the steps from the link and ensure that the option "Business" is chosen every time it is requested.

### 1.3 Create an App in the Meta Developer Dashboard  
https://developers.facebook.com/apps/  
Follow the steps and select the Business Manager account. In the "Use cases" step, select the "Use the old version" option.

### 1.4 Add a product  
In the new app, click "Add product" and then "Set up". Follow the steps.

### 1.5 Set permissions  
In Tools > Graph API Explorer, add the permissions:  
pages_show_list  
instagram_basic  
instagram_content_publish  
pages_read_engagement  
pages_manage_posts

### 1.6 Generate Access Token  
In the Graph API Explorer, click on “Generate access token”. Save it in a .env file as ACCESS_TOKEN=<my_token>.  
Tip: Debug the access token and set it to last 60 days. Otherwise, it will expire in only 2 hours.

### 1.7 Request the Instagram ID  
On the same page, at the URL line, select and type:

GET https://graph.facebook.com/v19.0/me/accounts?access_token=<my_token>

Then:
GET https://graph.facebook.com/v19.0/PAGE_ID?fields=instagram_business_account&access_token=<my_token>

Save the returned ID in the same .env file as INSTAGRAM_ACCOUNT_ID=<my_id>


## 2. Write a script to post on Instagram using their Meta Graph API.

In VS Code, write code for the following steps:

### 2.1 Import libraries
from dotenv import load_dotenv
import os
from pathlib import Path
import random
import requests
from datetime import datetime

### 2.2 Access external links
Load the tokens saved in the .env file.
Read and store the image's URL in a list. The Instagram API only posts from published images, not from local files.
Randomly select an image and its corresponding caption. (in progress)

```python
# accessing the tokens 
load_dotenv() 
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN") 
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID") 

# getting images 
folder_path = Path('/Users/aliceviggiani/Dropbox/1 estudos/5 data viz/0 master/pratt/2.5 2025 summer/697-botz/2-assignments/3 maprobot/img_resized') 

image_urls = [] 

for f in folder_path.iterdir(): 
    file_name = f.name url_gh = f'https://aliceaviggiani.github.io/map-bot/img_resized/{file_name}' 
    image_urls.append(url_gh) # selecting the post content to upload image_url = random.choice(image_urls) 
    
caption = 'Posted from the Internet Archive metadata by a bot.'
```


### 2.3 Create the post content in the API requested format
Create a dictionary with the image URL, caption, and token. Request a post to the Instagram Graph API by providing the posting URL combined with the Instagram ID created, along with the dictionary containing the content.

```python 
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
```

### 2.4 Getting the post ID
Request the "id" from the .json format of the previous request, and extract the "id" from the dictionary created by the .json parsed (The ID is the only element in the dictionary). Create a dictionary with the necessary information for posting: the post ID and the token.


```python
# geting the id of the post
post_id = post_request.json().get("id")

url_publish = f"https://graph.facebook.com/v19.0/{INSTAGRAM_ACCOUNT_ID}/media_publish"

publish_wrap = {
    'creation_id': post_id,
    'access_token': ACCESS_TOKEN
}
```

### 2.5 Post it! 
Request to the Graph API to post, providing the URL and access codes.
Tip: To track your schedule posts, print the time that was created so that it appears in the .log file (explained ahead). 

```python
# publishing!
publish_request = requests.post(url_publish, data=publish_wrap)
if publish_request.status_code != 200:
    print("Error:", publish_request.text)
    exit()

time = datetime.now().strftime("%m/%d/%Y at %H:%M")
print(f'It worked on {time} with the post id: {post_id} :)')
```


## 3. Write a configuration file .plist to run the script at a specified frequency.

After writing the script that enables posting on Instagram using their official API, which is managed directly by code, a task can be created and saved in a .plist file, allowing it to execute the script periodically.

### 3.1 Create a .plist file
On VS Code, create a .plist file and save it in the LaunchAgents folder on a Mac computer.
.plist stands for Property List, and it is a configuration file containing a list of defined instructions. In this case, it will instruct the launch of a script at 8 am daily.

### 3.2 Store the file in the Library folder
Save the file in: Users > “my user” > Library > LaunchAgents.
Note: It must be the user's library, not the system's one.
Also, it's necessary to verify the Python version used and ensure it's running properly. This script uses /opt/anaconda3/bin/python3.

### 3.3 Write the task in the .plist file
In VS Code, write the code in XML language, following the steps:

Set up the code.
Create a dictionary inside a plist tag. 
The dictionary must contain the following information: Label (file name), arguments (Python version used and script file path), time to trigger the task, and paths to the .log and .err files. The iOS system automatically creates these two files, and they store the log, historical, and eventual errors.

### 3.4 Copy and paste the code

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" 
"http://www.apple.com/DTDs/PropertyList-1.0.dtd">

<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.alice.instagrambot</string>

  <key>ProgramArguments</key>
  <array>
    <string>/opt/anaconda3/bin/python3</string>
    <string>/Users/aliceviggiani/Dropbox/1 estudos/5 data viz/0 master/pratt/2.5 2025 summer/697-botz/2-assignments/3 maprobot/697-mapposter-2.py</string>
  </array>

  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key>
    <integer>8</integer>
    <key>Minute</key>
    <integer>0</integer>
  </dict>

  <key>StandardOutPath</key>
  <string>/Users/aliceviggiani/Dropbox/1 estudos/5 data viz/0 master/pratt/2.5 2025 summer/697-botz/2-assignments/3 maprobot/instabot.log</string>

  <key>StandardErrorPath</key>
  <string>/Users/aliceviggiani/Dropbox/1 estudos/5 data viz/0 master/pratt/2.5 2025 summer/697-botz/2-assignments/3 maprobot/instabot.err</string>
</dict>
</plist>
```

### 3.5 Test the automation before 8am
To execute the .plist configuration before the time scheduled, type the following in the Terminal: launchctl start com.alice.instagrambot

Done : )


## 4. Write a script to download a set of images from an Internet Archive search using their API, in accordance with Instagram's requirements.

Create a notebook Python file and copy the script:

```python 
pip install internetarchive

from internetarchive import download
from internetarchive import get_item
import requests
import os
import pandas as pd
from io import BytesIO
from PIL import Image

# query path

search = 'map'
subject = 'data visualization'

params = {
    'q': f'({search}) AND subject:("{subject}") AND mediatype:(image)',
    'fl[]': 'identifier',
    'rows': 100,
    # 'sort[]': 'views desc',
    'sort[]': 'downloads desc', 
    'output': 'json'
}

search_url = 'https://archive.org/advancedsearch.php'
response = requests.get(search_url, params=params)
results = response.json()['response']['docs']

identifiers = [doc.get('identifier') for doc in results]
print(f"Found {len(identifiers)} items.")


# loop to download the largest image files for each item in the search result

download_dir = '/Users/aliceviggiani/Dropbox/1 estudos/5 data viz/0 master/pratt/2.5 2025 summer/697-botz/2-assignments/3 maprobot/img_original'

urls = []

for i in identifiers:
    item = get_item(i)
    sizes = []
    names = []

    for f in item.files:
        if f['name'].lower().endswith(('.jpg', '.jpeg', '.png')):
            sizes.append(int(f['size']))
            names.append(f['name'])

    if sizes:
        index = sizes.index(max(sizes))   
        largest_file = item.get_file(names[index])
        largest_file.download(
            destdir='/Users/aliceviggiani/Dropbox/1 estudos/5 data viz/0 master/pratt/2.5 2025 summer/697-botz/2-assignments/3 maprobot/img_original')
        urls.append(largest_file.url)
    else:
        print("Error")


# resizing image to fit Instagram aspect ratio

# accepted format on Instagram:
# width: 320 - 1080 pixels
# height: 566 – 1350
# aspect ratio 1.91:1 – 4:5 

def resize(image):
    # original dimensions
    width, height = image.size
    ratio = width / height

    # maximum format accepted by instagram
    width_max = 1080
    ratio_min = 0.8
    ratio_max = 1.91

    # resize if needed, while keeping the same ratio 
    if width > width_max or not(ratio_min <= ratio <= ratio_max):
        image.thumbnail((width_max, width_max), Image.LANCZOS)
        return image
    else:
        return image


for u in urls:
    response = requests.get(u)
    image_original = Image.open(BytesIO(response.content))

    image_resized = resize(image_original)

    filename = os.path.basename(u)
    save_path = os.path.join('/Users/aliceviggiani/Dropbox/1 estudos/5 data viz/0 master/pratt/2.5 2025 summer/697-botz/2-assignments/3 maprobot/img_resized', f'{filename}')
    image_resized.save(save_path)

# loop to get info for the legends

titles = []
dates = []
# descriptions = []
subjects = []
languages = []
collections = []

for i in identifiers:
    item = get_item(i)

    title = item.metadata.get('title', '[None]')
    date = item.metadata.get('date', '[None]')
    description = item.metadata.get('description', '[None]')
    subject = item.metadata.get('subject', '[None]')
    language = item.metadata.get('language', '[None]')
    collection = item.metadata.get('collection', '[None]')
    
    titles.append(title)
    dates.append(date)
    # descriptions.append(description)
    subjects.append(subject)
    languages.append(language)
    collections.append(collection)


def hashtags(subjects):
    if isinstance(subjects, list):
        result = []
        for s in subjects:
            if isinstance(s, list):
                group = ' '.join(f"#{str(i).lower().replace(' ', '')}" for i in s)
                result.append(group)
            else:
                result.append(f"#{str(s).lower().replace(' ', '')}")
        return result
    
    elif isinstance(subjects, str):
        return [f"#{subjects.lower().replace(' ', '')}"]
    
    else:
        return []

keywords = hashtags(subjects)

df = pd.DataFrame({
    'identifier': identifiers,
    'title': titles,
    'date': dates,
    'language': languages,
    'collection': collections,
    'url': urls,
    'keywords': keywords
})

df.to_csv(f"{download_dir}/{'ia-metadata-1.csv'}", index=False)
```


## Further developments:
1. Formatting and uploading proper captions.
2. Create a .log file to record posted images and exclude them from the following random selection.
3. Improve the process of resizing or cropping.
4. Make a carousel post with a cropped detail as the first image and the full version as the second.
5. Automate uploading images to GitHub.
