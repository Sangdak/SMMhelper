# SMMhelper 
This project is an SMM helper, that works with Google sheets, allows you to publish posts on your social media depending on the specified date and time.

## At first
1. `Python3` should already be installed.
2. Create .env file and add this:
   
   ```
   TG_API_TOKEN=<your tg_api_token>
   TG_CHAT_ID=<your tg_chat_id>
   VK_ACCESS_TOKEN=<your vk_access_token>
   VK_GROUP_ID=<your vk_group_id>
   ```

3. To make the script work correctly, you need to get the Google API key by following the [instructions.](https://github.com/Sangdak/SMMhelper/blob/master/instruction%20for%20google%20api.md)
   
   Next you need to create google sheets like this:
   ![image-2023-03-26-15-44-57.png](https://i.postimg.cc/Jhr0NY8Y/image-2023-03-26-15-44-57.png)
   
   and create images and texts directories in your Google Drive.
 
4. Download this repository. 
5. Install dependencies using:
  
   `pip3 install -r requirements.txt`

## Running the script

1. In file [google_api.py](https://github.com/Sangdak/SMMhelper/blob/master/google_api.py) we have 4 constant:
   
   `CREDENTIALS_FILE` - the path to your `creds.json` file 
   
   `SPREADSHEET_ID` - ID of your Google Sheets
   
   `IMG_FOLDER_ID` - ID of your Google Drive directory of images
   
   `TEXT_FOLDER_ID` - ID of your Google Drive directory of texts
   
   You need to put your values here.

2. Choose time and date in your Google Sheets, put links of image and text to the appropriate column and run the script using

3. 
``` python
python3 main.py
```































This repository was created as part of the Devman Education Project. Group work.
