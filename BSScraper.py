from __future__ import unicode_literals
from bs4 import BeautifulSoup
import re
import os
from PIL import Image
from lxml import etree
import urllib
import youtube_dl
import requests
from openpyxl import load_workbook
import dropbox
import shutil

#TODO Change the provided path to the path where the videos are saved.
videoPath = "/Volumes/Indie/Videos/"
#TODO Change the provided path to the path where you want to move the videos once they are successfully uploaded to DropBox.
movePath = "/Volumes/Indie/VideoDemo/"
#TODO Change the provided path to the path where you want to upload the videos on DropBox. This should be a DROPBOX location.
target = "/Backups/IndiegogoVideos/"
#TODO Change the provided path to the path where the webpages are saved.
path = "/Volumes/Indie/Webpages/"
#TODO Change the provided path to the path where you want to move the webpage once they are successfully processed.
moveWPPath = "/Volumes/Indie/Demo/"
#TODO Change the provided name to the name of your excel workbook.
wb = load_workbook("Demo.xlsx")
#TODO Change the provided name to the name of your excel sheet.
ws = wb.get_sheet_by_name("test")

# Status update after downloading the video from youtube
def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

'''
 If image exists, return 1 and the url
 If Video exists, return 2 and a dictionary containing the video_id and video_type (youtube/vimeo) as the keys 
 with the video id and type as values
 If there is nothing, return -1 and an empty string
'''
# TODO Uncomment the commented lines in the function to check for images
def getDetails(cdata):
    dict = {}
    for s in cdata.split(';'):
        i = 0
        if "pitch_video" in s:
            s = s.replace("\"", "")
            # if s.split("pitch_image:")[1].split(',', 1)[0] != 'null':
            #     flag = 1
            #     img = s.split("pitch_image:")[1].split("full_url:")[1].split('}', 1)[0]
            #     return flag, img
            if s.split("pitch_video:")[1].split(',', 1)[0] != 'null':
                flag = 2
                for str in s.split("pitch_video:")[1].split('{', 1)[1].split('}', 1)[0].split(','):
                    if i > 0:
                        dict[str.split(':', 1)[0]] = str.split(':', 1)[1]
                    i += 1
                return flag, dict
            return -1, ""

'''
 Returns alternate youtube video IDs 
'''
def getAltID(cdata, id):
    altID = []
    for s in cdata.split(';'):
        s = s.replace("\"", "")
        if s.startswith("gon.campaign="):
            for str in s.split("=",1)[1].split('gallery:', 1)[1].split('thumbnail_url'):
                strng = str.split(':\\')[0].split(':', 1)[1].split(',')[0]
                if strng.startswith("https://i3.ytimg.com/vi/"):
                    vid_id = strng.split('https://i3.ytimg.com/vi/')[1].replace('/default.jpg', "")
                    if vid_id != id:
                        altID.append(vid_id)

    return altID

'''
 Downloads and saves image in .jpg format
 If unsuccessful in saving the image, then the filename is logged for verification
'''

def downloadImg(ImgUrl, fileID):
    # TODO change the provided path here to the path where you want to save the image. Make sure that you change the path throughout this function
    img = urllib.urlretrieve(ImgUrl, '/Volumes/Indie/Images/' + str(fileID) + ".jpg")
    try:
        img1 = Image.open("/Volumes/Indie/Images/" + str(fileID) + ".jpg").convert('RGB').save("/Volumes/Indie/Images/" + str(fileID) + ".jpg")
        img1 = Image.open("/Volumes/Indie/Images/" + str(fileID) + ".jpg")
        img1.thumbnail((695, 460), Image.ANTIALIAS)
        img1.save('/Volumes/Indie/Images/' + str(fileID) + ".jpg", "JPEG")
        return 1
    except:
        outputFile = open("Log.txt", "a")
        outputFile.write(filename + "\n")
        outputFile.close()
        return 0

'''
 Returns true if the youtube link is valid
 Returns false if the youtube link is invalid
'''
def checkYTValidity(youtubeLink):
    youtube = etree.HTML(urllib.urlopen(youtubeLink).read())
    video_title = youtube.xpath("//span[@id='eow-title']/@title")
    if video_title:
        return True
    return False

'''
 Returns true if the vimeo link is valid
 Returns false if the vimeo link is invalid
 Data for excel sheet is recorded based on the validity of the vimeo link
'''
# TODO Uncomment the commented line in the function to download images
def checkVimeoValidity(vimeoLink, id, fileID):
    try:
        rowDets = []
        rowDets.append(1)
        rowDets.append("http://vimeo.com/" + id)
        rowDets.append(0)
        writeXLSX(rowDets, fileID)
        wb.save("Demo.xlsx")
        data = requests.get(vimeoLink +'.json').json()
        # downloadImg(data[0]['thumbnail_large'], fileID)
        return True
    except:
        rowDets = []
        rowDets.append(0)
        rowDets.append("NA")
        rowDets.append("NA")
        writeXLSX(rowDets, fileID)
        wb.save("Demo.xlsx")
        return False

'''
 Fills in the excel sheet row with the recorded data
'''
def writeXLSX(rowDets, fileID):
    i = 0
    for row in ws.rows:
        if i > 0:
            if row[0].value == fileID:
                row[3].value = rowDets[0]
                row[4].value = rowDets[1]
                row[5].value = rowDets[2]
                row[6].value = rowDets[3]
        i += 1

'''
 Uploads the file(s) in the given directory to dropbox.
'''
def dropboxUpload():
    # TODO Use your access token here.
    d = dropbox.Dropbox('your_access_token_goes here')
    for file in os.listdir(videoPath):
        if file != '.DS_Store':
            fn = file.rsplit('.', 1)[1]
            if (fn != 'part'):
                f = open(videoPath + file)
                targetfile = target + file
                print "Uploading: " + file
                file_size = os.path.getsize(videoPath + file)
                CHUNK_SIZE = 4 * 1024 * 1024
                if file_size <= CHUNK_SIZE:
                    d.files_upload(f.read(), targetfile, mode=dropbox.files.WriteMode("overwrite"))
                else:
                    upload_session_start_result = d.files_upload_session_start(f.read(CHUNK_SIZE))
                    cursor = dropbox.files.UploadSessionCursor(
                        session_id=upload_session_start_result.session_id, offset=f.tell())
                    commit = dropbox.files.CommitInfo(path=targetfile, mode=dropbox.files.WriteMode("overwrite"))
                    while f.tell() < file_size:
                        if ((file_size - f.tell()) <= CHUNK_SIZE):
                            d.files_upload_session_finish(f.read(CHUNK_SIZE),
                                                          cursor,
                                                          commit)
                        else:
                            d.files_upload_session_append_v2(f.read(CHUNK_SIZE),
                                                             cursor,
                                                             False)
                            cursor.offset = f.tell()
                shutil.move(videoPath + file, movePath + file)
            else:
                printLog(filename.encode('utf-8'))

'''
 Returns the ID of a filename from the excel sheet
'''
def getFileID(filename):
    i = 0
    fileID = ''
    for row in ws.rows:
        if i > 0:
            r = str(row[1].value)
            if(r != None):
                if " ".join(r
                                .replace(':', '_')
                                .replace('?', '_')
                                .replace('*', '_').split()) == " ".join(filename.rsplit('_', 1)[0].strip()
                                                                                                   .replace(',', '')
                                                                                                   .replace('&amp;','&')
                                                                                                   .split()):
                    fileID = row[0].value
                    break
        i += 1
    return fileID

'''
 If there is a problem with the file, then the filename is logged for verification.
'''
def printLog(filename):
    outputFile = open("Log.txt", "a")
    outputFile.write(filename + "\n")
    outputFile.close()

for filename in os.listdir(path):
     # Filter to process only html or htm files
     if (filename.endswith('.html') or filename.endswith('.htm')) and (not filename.startswith('._')):
        
        rowDets = []
        print filename
        f = open(path+filename)
        soup = BeautifulSoup(f, 'html.parser')
        f.close()
        fileID = getFileID(filename.rsplit('.', 1)[0])
        # All the pitch information is stored in CDATA. So, get that.
        cdatas = soup.findAll(text=re.compile("CDATA"))
        for cdata in cdatas:
            details = getDetails(cdata)
            if details != None:
                break
        # If the filename doesn't exist in the excel sheet or there is no image or video on the html page,
        # log the filename for verification.
        if fileID == '' or details[0] == -1:
            printLog(filename)
            continue
        if(details[0] == 1):

            rowDets.append(0)
            rowDets.append("NA")
            rowDets.append(1)
            rowDets.append(0)
            # Check if image exists or not
            if details[1] == "projects/missing/full.png":
                rowDets.append(0)
            else:
                val = downloadImg(details[1], fileID)
                rowDets.append(val)
            rowDets.append("NA")
            rowDets.append("NA")
            writeXLSX(rowDets, fileID)
            wb.save("Demo.xlsx")
        else:
            if details[1].get('video_type') == 'youtube':
                # set up options for the video to be downloaded. (video in .mp4 format, fileID as the name)
                # TODO Change the provided path in outtmpl to the path where you want to save the video.
                ydl_opts = {'format': 'best[ext=mp4]/best',
                            'outtmpl': '/Volumes/Indie/Videos/' + str(fileID) + '.%(ext)s',
                            'noplaylist': True,
                            'progress_hooks': [my_hook], }
                if checkYTValidity("https://youtu.be/" + details[1].get('video_id')):
                    rowDets.append(1)
                    rowDets.append("https://youtu.be/" + details[1].get('video_id'))
                    rowDets.append(1)
                    writeXLSX(rowDets, fileID)
                    wb.save("Demo.xlsx")
                    # Start downloading the video using the obtained video id. In case of connection failures, retry 5
                    # times before logging the filename for verification.
                    # TODO Uncomment the lines calling downloadImg method to download images
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        try:
                            info_dict = ydl.extract_info("https://www.youtube.com/watch?v=" + details[1].get('video_id'))
                            # downloadImg(info_dict['thumbnails'][0]['url'], fileID)
                        except:
                            j = 0
                            while (j <= 5):
                                try:
                                    info_dict = ydl.extract_info("https://www.youtube.com/watch?v=" + details[1].get('video_id'))
                                    # downloadImg(info_dict['thumbnails'][0]['url'], fileID)
                                    break
                                except:
                                    j+=1
                            if(j == 5):
                                print("All retries failed. Try later")
                                printLog(filename)


                else:
                    # TODO Uncomment the following commented lines to get the alternate voutube ids and download the images.
                    rowDets.append(0)
                    rowDets.append('NA')
                    rowDets.append("NA")
                    writeXLSX(rowDets, fileID)
                    wb.save("Demo.xlsx")
                    # altID = getAltID(cdata, details[1].get('video_id'))
                    # if altID:
                    #     for id in altID:
                    #         if checkYTValidity("https://youtu.be/" + id):
                    #             with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    #                         info_dict = ydl.extract_info("https://www.youtube.com/watch?v="+id, download=False)
                    #                         # downloadImg(info_dict['thumbnails'][0]['url'], fileID)
                    #             break
                dropboxUpload()
            elif details[1].get('video_type') == 'vimeo':
                checkVimeoValidity('http://vimeo.com/api/v2/video/' + details[1].get('video_id'), details[1].get('video_id'), fileID)
     # Move the file out of the directory to some other directory.
     if (not filename.startswith('._')):
        shutil.move(path + filename, moveWPPath + filename)
wb.save("Demo.xlsx")












