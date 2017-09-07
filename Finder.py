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

def getFile(filename):
    i = 0
    fileID = ''
    for row in ws.rows:
        if i > 0:
            # print(row[1].value)
            r = str(row[1].value)
            if(r != None):
                if " ".join(r
                                .replace(':', '_')
                                .replace('?', '_')
                                .replace('*', '_').split()) == " ".join(filename.rsplit('_', 1)[0].strip()
                                                                                                   .replace(',', '')
                                                                                                   .replace('&amp;','&')
                                                                                                    .split()):
                    print "Moving File: ", filename
                    shutil.move(path + filename, moveWPPath + filename)
                    break
        i += 1
    return fileID

wb = load_workbook("test.xlsx")
ws = wb.get_sheet_by_name("test")
moveWPPath = "/Volumes/Indie/Webpages/"
path = "/Volumes/Indie/Old WP/"

for filename in os.listdir(path):
    if (filename.endswith('.html') or filename.endswith('.htm')) and (not filename.startswith('._')):
        getFile(filename)