import os, exifread, shutil ,time, rawpy, tempfile, cv2
from PIL import Image
from pathlib import Path


class application:

    def __init__(self,destination) -> None:
        self.extensions = ('.dng', '.raw', '.cr2', '.crw', '.erf', '.raf', '.tif', '.kdc', '.dcr', '.mos',
                                    '.mef', '.nef', '.orf', '.rw2', '.pef', '.x3f', '.srw', '.srf', '.sr2', '.arw',
                                    '.mdc', '.mrw')
        self.face_cascade = cv2.CascadeClassifier("E:\project\FOrg\haarcascade\haarcascade_frontalface_alt.xml")


    def createDatabase(self,dir):
        Database = {}
        for root, dirs, files in os.walk(dir):
            for file in files:
                if file.endswith(self.extenstions):
                    location = f"{root}\\{file}"
                    f = open(location, 'rb')
                    tags = exifread.process_file(f)

                    Database[file] = {
                        "root" : location,
                        "ext"  : Path(file).suffix,
                        "Model" :  ("%s" % tags["Image Model"]),
                        "FocalLength": ("%s" % tags["EXIF FocalLength"]),
                        "ISO": ("%s" % tags["EXIF ISOSpeedRatings"]),
                        "Fstop": ("%s" % tags["EXIF FNumber"]),
                        "Date & Time": ("%s" % tags["EXIF DateTimeDigitized"]),
                        "Potrait": self.
                        }
                    f.close()
        return Database

    def view_preview(self,address):
        with rawpy.imread(address) as raw:
            try:
                thumb = raw.extract_thumb()
            except rawpy.LibRawNoThumbnailError:
                print('no thumbnail found')
            except rawpy.LibRawUnsupportedThumbnailError:
                print('unsupported thumbnail')
            else:
                with tempfile.NamedTemporaryFile() as tmp:
                    tmp.write(thumb.data)
                    img = Image.open(tmp)
                    img.show()
    
    def process_photo(self,database,sortValue,targetPath):
        processedPhotos = 0
        for file,tags in database.items():
            destinationFolder = tags[sortValue]
            if not os.path.isdir(os.path.abspath(os.path.join(targetPath, destinationFolder))):
                os.makedirs(os.path.abspath(os.path.join(targetPath, destinationFolder)))
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