import os
from pathlib import Path
path ="E:\project\FOrg\lol"
if not os.path.isdir(path):
    os.mkdir(path)
Path("E:\project\FOrg\preview.py").rename("E:\project\FOrg\lol\preview.py")



