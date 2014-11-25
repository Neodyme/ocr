import glob, os

if __name__=="__main__":
    for i in glob.glob(os.path.join("./", "*.bmp")):
        title, ext = os.path.splitext(os.path.basename(i))
        os.rename(i, (chr(ord(title[0])) + ".bmp"))
