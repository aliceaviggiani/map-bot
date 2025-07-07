# 697 Botz  
**July 6, 2025**  
**Alice Viggiani**

## A bot to daily post good references for map design from the Internet Archive metadata on Instagram

---

### Tutorial

To build a bot that automatically posts once a day on Instagram, using Internet Archive metadata as a source, and programming with Python on an iMac, it will need to:

1. Set up a Meta Developer environment and accounts as specified, and fulfill other necessary requirements.  
2. Write a script to automate an Instagram post using the Meta Graph API.  
3. Write a configuration in a `.plist` file to schedule a trigger that runs the script and save it in the `LaunchAgents` folder on a Mac computer.  
4. Write a script to download a set of images from an Internet Archive search using their API, in accordance with Instagram's requirements.  
5. Upload and publish the resulting images in a GitHub repository.  
6. Update the first script with the actual images.  
7. Repeat steps 4 to 6 when new images are needed.

Check out the bot: [@undr.constrctn](https://www.instagram.com/undr.constrctn)

---

### Further developments:
- Formatting and uploading proper captions.  
- Create a `.log` file to record posted images and exclude them from the following random selection.  
- Improve the process of resizing or cropping.  
- Make a carousel post with a cropped detail as the first image and the full version as the second.  
- Automate uploading images to GitHub.

---

This tutorial focuses on **steps 1 to 3**.

---

## 1. Set up a Meta for Developers environment

### 1.1 Create and connect accounts

From a mobile:

- Create the following accounts:
  - **Instagram Business** (choose the "business" option when creating)
  - **Facebook** (personal is enough)
  - **Facebook Page**
- Link them in: `Facebook > Settings > Linked accounts`

### 1.2 Create a Meta Developer account

[Meta Developer Signup](https://business.facebook.com/business/loginpage/?next=https%3A%2F%2Fdevelopers.facebook.com%2Fasync%2Fregistration#)  
Follow the steps and always choose the **Business** option when prompted.

### 1.3 Create an App in the Meta Developer Dashboard

[Apps Dashboard](https://developers.facebook.com/apps/)  
Create a new App and select your **Business Manager** account.  
At the "Use cases" step, select **"Use the old version"**.

### 1.4 Add a product

- In your new app, click **"Add product"** → **"Set up"**
- Follow the setup process

### 1.5 Set permissions

In **Tools > Graph API Explorer**, add these permissions:

- `pages_show_list`
- `instagram_basic`
- `instagram_content_publish`
- `pages_read_engagement`
- `pages_manage_posts`

### 1.6 Generate Access Token

- In **Graph API Explorer**, click **Generate Access Token**
- Save it in a `.env` file:
  ```env
  ACCESS_TOKEN=<my_token>
