import os
import zipfile

def zipdir(path, filename):
    ziph = zipfile.ZipFile(filename + '.zip', 'w', zipfile.ZIP_DEFLATED)
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        print(root,dirs,files)
        for file in files:
            ziph.write(os.path.join(root, file),os.path.relpath(os.path.join(root, file),os.path.join('..',path)))

