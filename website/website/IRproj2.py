import os
import re
import fileinput
import json
import math
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

def calDF():
    dfdict = {}
    with open('tfRecording.json') as json_file:
        data = json.load(json_file)
        for name in data:
            for word in data[name]:
                if word not in dfdict:
                    dfdict[word] = 1
                else:
                    dfdict[word] += 1
    json_str = json.dumps(dfdict)
    try:
        f = open('dfRecording.json', 'w')
        f.write(json_str)
        f.close()
    except BaseException as e:
        print("error: " + e)

def calNormalized():
    normalizeddict = {}
    with open('tfRecording.json') as json_file:
        data = json.load(json_file)
        for name in data:
            sum = 0
            tmp = {}
            for word in data[name]:
                sum = sum + 1 + math.log10(data[name][word])
            for word in data[name]:
                tmp[word] = (1 + math.log10(data[name][word]))/math.sqrt(sum)
            normalizeddict[name] = tmp
    json_str = json.dumps(normalizeddict)
    try:
        f = open('normalizedRecording.json','w')
        f.write(json_str)
        f.close()
    except BaseException as e:
        print("error: " + e)
            
def query(word):
    wordlist = word.lower().split()
    scorelist = {}
    with open('dfRecording.json') as df_file:
        df = json.load(df_file)
        with open('tfRecording.json') as tf_file:
            tf = json.load(tf_file)
            with open('normalizedRecording.json') as n_file:
                norm = json.load(n_file)
                for name in norm:
                    score = 0
                    for wd in wordlist:
                        if wd in norm[name]:
                            score += ((1+math.log10(tf[name][wd]))*math.log10(12.0/df[wd]))*norm[name][wd]
                    scorelist[name] = score * 1000
    return scorelist

def sortlist(scorelist):
    
    dict= sorted(scorelist.items(), key=lambda d:d[1], reverse = True)
    for i in dict:
        print(i)
                        

if __name__ == '__main__':
    #calTF('./papertxt')
    #calDF()
    #calNormalized()
    a = "5G mobile"
    sortlist(query(a))