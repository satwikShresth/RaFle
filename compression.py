import sys
from PIL import Image
import os
import threading as thread
import rawpy
import imageio
from datetime import datetime
import optparse

class raw_to_jpeg:
  # create a message function
  def __init__(self,directory = "converted"):
    self.screenLock = thread.Semaphore(value=1)
    self.directory = directory
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
  def message(self,file, bool):
      self.screenLock.acquire()
      # if is converted
      if bool:
          print(datetime.now().time().strftime('%H:%M:%S') + " Converted:  " + file)
      else:
          print(datetime.now().time().strftime('%H:%M:%S') + " Converting:  " + file)
      self.screenLock.release()
  
  
  # create a directory if needed to store our converted images!
  
  
  
  # convert RAW images function
  def convert_raw(self,file, directory, tgtDir, extension=".jpg"):
      # path = 'image.nef'
  
      try:
          self.message(file, False)
          path = os.path.join(tgtDir, file)
          with rawpy.imread(path) as raw:
              rgb = raw.postprocess()
          imageio.imsave(os.path.join(directory, file + extension), rgb)
          self.message(file, True)
      except:
          pass
  
  
  # convert function
  def convert_file(self,file, directory, tgtDir):
      try:
          self.message(file, False)
          path = os.path.join(tgtDir, file)
          im = Image.open(path)
          # basewidth = 2048
          # wpercent = (basewidth/float(im.size[0]))
          # hsize = int((float(im.size[1])*float(wpercent)))
          # im = im.resize((basewidth,hsize), Image.ANTIALIAS)
          im.save(os.path.join(directory, file + ".jpg"), "JPEG", dpi=(600, 600))
          self.message(file, True)
  
      except:
          pass
  
  # IT IS POINTLESS TO CONVERT WHAT IS ALREADY CONVERTED!!!!
  def image_not_exists(self,e):
      if os.path.isfile(os.path.join(self.directory, e + '.jpg')):
          self.screenLock.acquire()
          print("File " + e + " is already converted! \n")
          self.screenLock.release()
          return False
      else:
          return True
  
  
  # here we check each file to decide what to do		
  def checkExtension(ext):
      # set supported raw conversion extensions!
      extensionsForRawConversion = ['.dng', '.raw', '.cr2', '.crw', '.erf', '.raf', '.tif', '.kdc', '.dcr', '.mos',
                                    '.mef', '.nef', '.orf', '.rw2', '.pef', '.x3f', '.srw', '.srf', '.sr2', '.arw',
                                    '.mdc', '.mrw']
    
      for i in extensionsForRawConversion:
          if ext.lower().endswith(i):
              return 'RAW'


def main():
  print('### PYTHON IMAGE CONVERTER ### \n \n')
  parser = optparse.OptionParser("usage: " + sys.argv[0] + \
                                   "\n-s <source directory> \n ex: usage%prog -s C:\\Users\\USerName\\Desktop\\Photos_Dir \n After -s Specify the directory you will convert")
  parser.add_option('--s', dest='nname', type='string', \
                    help='specify your source directory!')
  parser.add_option('--ext', dest='target_image_extension', type='choice', \
                    default=".jpg", choices = ['.jpg', '.png'], help='the image format to be used for the converted images.')
  (options, args) = parser.parse_args()
  rtj = raw_to_jpeg()
  if (options.nname == None):
    print(parser.usage)
    exit(0)
  else:
    tgtDir = os.path.abspath(options.nname)
  
  print("Started conversion at : " + datetime.now().time().strftime('%H:%M:%S') + '\n')
  print("Converting \n -> " + tgtDir + " Directory !\n")
    # find files to convert
  try:
    for file in os.listdir(tgtDir):
      # CHECK IF WE HAVE CONVERTED THIS IMAGE! IF YES SKIP THE CONVERSIONS!
      if rtj.image_not_exists(file):
        if 'RAW' == rtj.checkExtension(file):
          # Added multithreds to complete conversion faster
          t2 = thread.Thread(target=rtj.convert_raw, args=(file, rtj.directory, tgtDir, options.target_image_extension))
          t2.start();
          if 'NOT_RAW' == rtj.checkExtension(file):
            t = thread.Thread(target=rtj.convert_file, args=(file, rtj.directory, tgtDir))
            t.start();
          if file.endswith('.tif'):
            t = thread.Thread(target=rtj.convert_file, args=(file, rtj.directory, tgtDir))
            t.start();
          print(" \n Converted Images are stored at - > \n " + os.path.abspath(rtj.directory))
  except:
    print("\n The directory at : \n " + tgtDir + "  \n Are you sure is there? \n I am NOT! \n It NOT EXISTS !! Grrrr....\n\n")

if __name__ == '__main__':
    main()
