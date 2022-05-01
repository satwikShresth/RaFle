import os, cv2, shutil


print(os.getcwd())

os.chdir(r"D:\Exports for sony mausi\riya di single")
newpath = os.getcwd()
photos = os.listdir()
i = 1

face_cascade = cv2.CascadeClassifier("E:\project\FOrg\haarcascade\haarcascade_frontalface_alt.xml")
for photo in photos:
    if photo.endswith(".jpg"):
        print(str(i)+'.'+photo)
        photopath = os.path.join(newpath,photo)
        print(photopath)
        img = cv2.imread(photopath)
        scale_percent = 20
        dim = (int (img.shape[1]*scale_percent/100),int (img.shape[0]*scale_percent/100))
        rimage = cv2.resize(img,dim,interpolation= cv2.INTER_AREA)
        gray = cv2.cvtColor(rimage,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,1.1,4)
        numface = len(faces)
        print(numface)
        if numface==0:
            if not os.path.isdir(r"E:\project\FOrg\lol"):
                os.makedirs(r"E:\project\FOrg\lol")    
            shutil.move(photopath,(r'E:\project\FOrg\lol\%s' % photo))
        i += 1


def checkPotrait(destition,target):
    

