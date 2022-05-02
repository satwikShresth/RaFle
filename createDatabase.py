import os, exifread, shutil ,time, rawpy, tempfile, cv2
import numpy as np
from posixpath import split
from PIL import Image
from pathlib import Path 

class application:

    def __init__(self) -> None:
        self.extensions = ('.dng', '.raw', '.cr2', '.crw', '.erf', '.raf', '.tif', '.kdc', '.dcr', '.mos',
                                    '.mef', '.nef', '.orf', '.rw2', '.pef', '.x3f', '.srw', '.srf', '.sr2', '.arw',
                                    '.mdc', '.mrw', '.jpg', '.png')
        self.face_cascade = cv2.CascadeClassifier("E:\project\FOrg\haarcascade\haarcascade_frontalface_alt.xml")
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.valueTags = [
            "EXIF FocalLength",
            "EXIF ISOSpeedRatings",
            "EXIF FNumber",
            "EXIF DateTimeDigitized",
        ]
        self.faces= []
        self.labels=[]
        self.subject = ["","riya"]

    
    def predict(self,test_img):
        img = test_img.copy()
        face, rect = self.detect_face(img)
        label, confidence = self.face_recognizer.predict(face)
        label_text = self.subjects[label]
        self.draw_rectangle(img, rect)
        self.draw_text(img, label_text, rect[0], rect[1]-5)
        return img
    
    def draw_rectangle(self,img, rect):
        (x, y, w, h) = rect
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    def draw_text(self,img, text, x, y):
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

    def detect_face(self,img):
        image_array =np.array(img,"uint8")
        faces = self.face_cascade.detectMultiScale(image_array,scaleFactor=1.5 )
        if (len(faces) == 0):
            return None, None
        (x, y, w, h) = faces[0]
        return image_array[y:y+w, x:x+h], faces[0]

    def train_algo(self,database):
        labels = []
        for image_name in database.values():
            print(image_name["root"])
            if image_name["root"].endswith(("jpg","jpeg")):
                image = Image.open(image_name["root"]).convert("L")
                face, label = self.detect_face(image)
            if face is not None:
                self.faces.append(face)
                print(label)
                labels.append(label)
        print(np.array(labels))
        l = np.array(labels)
        self.face_recognizer.train(self.faces,l)
        

    def createDatabase(self,dir):
        Database = {}
        for root, dirs, files in os.walk(dir):
            for file in files:
                if file.endswith(self.extensions):
                    location = os.path.join(root,file)
                    f = open(location, 'rb')
                    self.tags = exifread.process_file(f)

                    Database[file] = {
                        "root" : location,
                        "ext"  : Path(file).suffix,
                        "Potrait": self.checkPotrait(location)
                        }
                    for i in self.valueTags:
                        taa =i.split(" ")
                        try:
                            Database[file][taa[-1]] = ("%s" % self.tags[i])
                        except:
                            continue
                    f.close()
        return Database
    
    def checkPotrait(self,destition,):
        img = cv2.imread(destition)
        scale_percent = 20
        dim = (int (img.shape[1]*scale_percent/100),int (img.shape[0]*scale_percent/100))
        rimage = cv2.resize(img,dim,interpolation= cv2.INTER_AREA)
        gray = cv2.cvtColor(rimage,cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray,1.1,4)
        numface = len(faces)
        if numface == 0:
            return "Landscape"
        else:
            return "Potrait"

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
        notprocessedPhotos = 0
        for file,tags in database.items():
            try:
                destinationFolder = tags[sortValue]
                if not os.path.isdir(os.path.abspath(os.path.join(targetPath, destinationFolder))):
                    os.makedirs(os.path.abspath(os.path.join(targetPath, destinationFolder)))
                newName = os.path.abspath(os.path.join(targetPath, destinationFolder,file))
                shutil.move(tags["root"],newName)
                processedPhotos += 1
            except:
                notprocessedPhotos +=1
            else:
                print("\r%d photos processed" % (processedPhotos), end='')
                print("\r%d photos processed" % (notprocessedPhotos), end='')
        
        
def main(argv=None):
    tic = time.perf_counter()
    dir = r"E:\project\FOrg\images"
    app = application()
    database = app.createDatabase(dir)
    print("There are total %d files" % len(database))
    app.process_photo(database, "Portrait",r"E:\project\lol")
    app.train_algo(database)
    test = cv2.imread(r"E:\project\FOrg\D2009094.jpg")
    app.predict(test)
    toc = time.perf_counter()
    print(f"Time used: {toc - tic:0.4f} seconds")


if __name__ == "__main__":
    main()