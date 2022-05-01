import exifread

# path to the image or video
imagename = r"E:\project\FOrg\D2009483.ARW"


# Open image file for reading (must be in binary mode)
f = open(imagename, 'rb')

# Return Exif tags
tags = exifread.process_file(f)

for tag in tags.keys():
    if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
        print ("Key: %s, value %s" % (tag, tags[tag]))
