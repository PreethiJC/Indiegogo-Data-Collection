from __future__ import unicode_literals
import os
from openpyxl import load_workbook
import shutil

#TODO Change the provided name to the name of your excel workbook.
wb = load_workbook("test.xlsx")
#TODO Change the provided name to the name of your excel sheet.
ws = wb.get_sheet_by_name("test")
#TODO Change the provided path to the path where you want to move the webpage once they are successfully processed.
moveWPPath = "/Volumes/Indie/Webpages/"
#TODO Change the provided path to the path where the webpages are saved.
path = "/Volumes/Indie/Old WP/"

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



for filename in os.listdir(path):
    if (filename.endswith('.html') or filename.endswith('.htm')) and (not filename.startswith('._')):
        getFile(filename)