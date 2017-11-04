import os
import re
import fileinput
import json
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams


def pdfTotxt1(filepath,outpath):
    try:
        fp = file(filepath, 'rb')
        outfp=file(outpath,'w')
        rsrcmgr = PDFResourceManager(caching = False)
        laparams = LAParams()
        device = TextConverter(rsrcmgr, outfp, codec='utf-8', laparams=laparams,imagewriter=None)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp, pagenos = set(),maxpages=0,
                                      password='',caching=False, check_extractable=True):
            page.rotate = page.rotate % 360
            interpreter.process_page(page)
        fp.close()

        device.close()
        outfp.flush()
        outfp.close()
    except Exception as e:
         print ("Exception:%s",e)


def pdfTotxt(fileDir):
    files=os.listdir(fileDir)
    tarDir=fileDir+'txt'
    if not os.path.exists(tarDir):
        os.mkdir(tarDir)
    replace=re.compile(r'/.pdf',re.I)
    for file in files:
        filePath=fileDir+'/'+file
        outPath=tarDir+'/'+re.sub(replace,'',file)+'.txt'
        pdfTotxt1(filePath,outPath)
        print ("Saved " + outPath)

def calTF(fileDir):
    files=os.listdir(fileDir)
    punctuation = {'\'s', '(', ')', ',', '.', '!', ':',
                   ';', '?', '--', '?', '\''}
    tfdict = {}
    for file in files:
        child = os.path.join(file)
        tmp = {}
        for line in fileinput.input(fileDir + '/' + child):
            for pun in punctuation:
                if pun in line:
                    line = line.replace(pun, ' ')
            for word in line.lower().split():
                if word not in tmp:
                    tmp[word] = 1
                else:
                    tmp[word] += 1
        tfdict[child[0:-5]] = tmp
    json_str = json.dumps(tfdict)
    try:
        f = open('tfRecording.json','w')
        f.write(json_str)
        f.close()
    except BaseException as e:
        print("error: " + e)
         

if __name__ == '__main__':
    calTF('./papertxt')