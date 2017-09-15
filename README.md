# Indiegogo-Data-Collection
Offline Scraping for Indiegogo website
#### BSScraper.py
The purpose of this program is to scrape the data from the webpages stored offline. It collects the video information and image information and fills an excel sheet with values pertaining to the image and video. For example, Does the video exist?, Video URL, Does the image exist?, Is it Vimeo video or YouTube video?, etc.

The following conditions are applied to extract the information from the webpage:
* *If the first frame contains a working YouTube video*  
  The program proceeds to download the video, and the video's cover image. It also updates the excel sheet with appropriate values.
* *If the first frame contains a working Vimeo video*  
  The program downloads the video's cover image. It also updates the excel sheet with appropriate values.
* *If the first frame is a working image*  
  The programs downloads the image and updates the excel sheet with appropriate values.
* *If the first frame is a broken image*  
  The program just updates the excel sheet with appropriate values
* *If the first frame contains a non-working YouTube video*  
  The program searches for the next frame that contains a working YouTube video and downloads only the image.
 

## Getting Started

Clone this repository.

    $ git clone https://github.com/PreethiJC/Indiegogo-Data-Collection.git

Install these libraries:
* Beautiful Soup 4
  ```
  $ pip install bs4
  ```
* Pillow
  ```
  $ pip install Pillow
  ```
* lxml
  ```
  $ pip install lxml
  ```
* youtube-dl
  ```
  $ pip install youtube_dl
  ```
* openpyxl
  ```
  $ pip install openpyxl
  ```
* dropbox
  ```
  $ pip install dropbox
  ```
## Prerequisites
* An excel sheet with the file id, project name, link to the project, <custom fields>
* Saved Webpages in html or htm format. Ensure that the webpages have the same name as the project name in the excel sheet.  
  >**Note:**  
  >*This program does not work on webpages that contain private vimeo videos in their first frame.*   

## Execution
1. Follow the TODO comments to make changes in the program to ensure that it runs on your system.

2. Run the individual programs.

    For example,

        $ python BSScraper.py 

## Author
Preethi Chavely
