# Indiegogo-Data-Collection
Offline Scraping for Indiegogo website

#### BSScraper.py
The purpose of this program is to scrape the data from the webpages stored offline. It collects the video information and image information and fills an excel sheet with values pertaining to the image and video. For example, Does the video exist?, Video URL, Does the image exist?, Is it Vimeo video or YouTube video?, etc.

The following conditions are applied to extract the information from the webpage:
* *If the first frame contains a working YouTube video*  
  The program proceeds to download the video, and the video's cover image. It also updates the excel sheet with appropriate values.
* *If the first frame contains a Vimeo video*  
  The program downloads the video's cover image. It also updates the excel sheet with appropriate values.
* *If the first frame is a working image*  
  The programs downloads the image and updates the excel sheet with appropriate values.
* *If the first frame is a broken image*  
  The program just updates the excel sheet with appropriate values
* *If the first frame contains a non-working YouTube video*  
  The program searches for the next frame that contains a working YouTube video and downloads only the image.
 
#### Randomizer.py
This is a small side project in the same Project. There is a CSV file that contains links to the campaigns on Indiegogo websites and the years when the campaigns started. These rows are sorted by the years.  

This program randomizes the rows in the CSV file such that, while collecting information of these campaigns, there is no overrepresentation of campaigns from any specific year. For example, the first campaign can be from 2013, the next campaign would be from 2016.  

#### Finder.py
This is also a small side project to help out the main Project. But this program does not impact the execution of BSScraper.py in any way.  

The program searches for html files that have the same name as the name in the 2nd column of the excel sheet and moves them from one directory to another.

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

## Execution Issues
If there is a problem in downloading a video, getting the File ID of a webpage, saving an image, or missing information, then the program saves the problem file's name in a file called Log.txt. You can go through these files manually to see what the problem is. 

## Author
Preethi Chavely
