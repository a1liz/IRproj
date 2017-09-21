import os

def eachFile(filepath):
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join(allDir)
        print(child)

if __name__ == '__main__':
    filePath = 'Shakespeare'
    eachFile(filePath)