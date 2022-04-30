import sys
import os
from PIL import Image 
import threading as thread
import rawpy
import imageio

with rawpy.imread('D2009483.ARW') as raw:
    try:
        thumb = raw.extract_thumb()
    except rawpy.LibRawNoThumbnailError:
        print('no thumbnail found')
    except rawpy.LibRawUnsupportedThumbnailError:
        print('unsupported thumbnail')
    else:
        if thumb.format == rawpy.ThumbFormat.JPEG:
            with open('thumb.jpg','wb') as f:
                f.write(thumb.data)
        elif thumb.format == rawpy.ThumbFormat.BITMAP:
            imageio.imsave('thumb.tiff',thumb.data)