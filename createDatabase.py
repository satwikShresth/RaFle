import os
import exifread
import os
from PIL import Image
import shutil
import time


def createDatabase(dir):
    Database = {}
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(r".ARW"):
                location = f"{root}\\{file}"
                f = open(location, 'rb')
                tags = exifread.process_file(f)

                Database[file] = {
                    "root" : location,
                    "Model" :  ("%s" % tags["Image Model"]),
                    "FocalLength": ("%s" % tags["EXIF FocalLength"]),
                    "ISO": ("%s" % tags["EXIF ISOSpeedRatings"]),
                    "Fstop": ("%s" % tags["EXIF FNumber"]),
                    "Date & Time": ("%s" % tags["EXIF DateTimeDigitized"])
                    }
                f.close()
    return Database



def process_photo(database,sortValue,targetPath):
    for file,tags in database.items():
        destinationFolder = tags[sortValue]
        if not os.path.isdir(os.path.abspath(os.path.join(targetPath, destinationFolder))):
            os.mkdir(os.path.abspath(os.path.join(targetPath, destinationFolder)))
        newName = os.path.abspath(os.path.join(targetPath, destinationFolder,file))
        shutil.move(tags["root"],newName)
        processedPhotos += 1
        print("\r%d photos processed" % (processedPhotos), end='')
        
def main(argv=None):
    tic = time.perf_counter()
    dir = r"E:\project"
    database = createDatabase(dir)
    print("There are total %d files" % len(database))
    process_photo(database, "Model",r"E:\project\lol")
    toc = time.perf_counter()
    print(f"Time used: {toc - tic:0.4f} seconds")


if __name__ == "__main__":
    main()