# SMMhelper 
This project is an SMM helper, that works with Google sheets, allows you to publish posts on your social media depending on the specified date and time.

## At first
1. `Python3` should already be installed.

3. To make the script work correctly, you need to get the Google API key by following the [instructions](https://github.com/Sangdak/SMMhelper/blob/master/instruction%20for%20google%20api.md),  Telegram API key, using [this](https://botcreators.ru/blog/botfather-instrukciya/) and VK API key, using [this](https://rdd.media/kak-poluchit-access_token-vkontakte/).
   
   Next you need to create google sheets like this:
   ![image-2023-03-26-15-44-57.png](https://i.postimg.cc/Jhr0NY8Y/image-2023-03-26-15-44-57.png)
   
   and images and texts directories in your Google Drive.

4. Download this repository. 
 
 2. Create .env file and add this:
  ```
  VK_API  
  VK_APP_CLIENT_ID=
  VK_ACCESS_TOKEN=
  VK_GROUP_ID=

 TG_API  
TG_API_TOKEN=
TG_CHAT_ID=

  GOOGLE_API
 CREDENTIALS_FILE=creds.json
 SPREADSHEET_ID=
 IMG_FOLDER_ID=
 TEXT_FOLDER_ID=

  MAIN
REFRESH_TABLE_PERIOD_SECONDS= 10
IMAGES_FOLDER_NAME=imgs
TEXTS_FOLDER_NAME=txts
```

5. Install dependencies using:
  
   `pip3 install -r requirements.txt`

## Running the script

1. Choose time and date in your Google Sheets, put links of image and text to the appropriate column and run the script using
   ```python
   python3 main.py
   ```































This repository was created as part of the Devman Education Project. Group work.
