import csv
import random

#TODO Change the provided path to the path where the csv file, whose rows have to be randomized, is stored.
inputPath = "/Users/Zion/iCloud Drive (Archive)/Desktop/Desktop - Zion/Job/Indiegogo/IndiegogoMusicProjects.csv"
outputPath = "randomVideo.csv"

rowList = []
yearList = []
newRowList =[]
with open(inputPath, "rb") as f:
    reader = csv.reader(f, delimiter=",")
    header = next(reader)
    for line in reader:
        rowList.append(line)
f.close()
for row in rowList:
    yearList.append(row[16])

randomIndices = random.sample(range(len(yearList)), len(yearList))

for i in randomIndices:
    newRowList.append(rowList[i])

with open(outputPath, "wb") as f:
    writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    print header
    writer.writerow(header)
    for row in newRowList:
        writer.writerow(row)
f.close()
