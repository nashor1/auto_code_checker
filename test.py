import os
os.chdir('./')


with open(file="static/upload/123.txt")as f:
    data = f.read()
    print(data)