import os
import fileinput
import pymysql
import json

def eachFile(filepath):
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join(allDir)
        print(child)



def transform_alabo2_roman_num(one_num):  
    ''''' 
    将阿拉伯数字转化为罗马数字 
    '''  
    num_list=[1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]  
    str_list=["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]  
    res=''  
    for i in range(len(num_list)):  
        while one_num>=num_list[i]:  
            one_num-=num_list[i]  
            res+=str_list[i]  
    return res  

def transform_roman_num2_alabo(one_str):  
    ''''' 
    将罗马数字转化为阿拉伯数字 
    '''  
    define_dict={'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}  
    if one_str=='0':  
        return 0  
    else:  
        res=0  
        for i in range(0,len(one_str)):  
            if i==0 or define_dict[one_str[i]]<=define_dict[one_str[i-1]]:  
                res+=define_dict[one_str[i]]  
            else:  
                res+=define_dict[one_str[i]]-2*define_dict[one_str[i-1]]  
        return res  
    
def connectDB():
    db = pymysql.connect('localhost','liz','qwer123','irdb')
    cursor = db


def createDocID():
    filePath = 'Shakespeare'
    pathDir = os.listdir(filePath)
    db = pymysql.connect(host='localhost',
                         port=3306,
                         user='root',
                         password='qwer123',
                         db='irdb')
    cursor = db.cursor()
    docID = 0
    for allDir in pathDir:
        child = os.path.join(allDir)
        act = 0
        scene = 0
        for line in fileinput.input(filePath + '/' + child):
            if line.strip() == 'ACT ' + transform_alabo2_roman_num(act + 1):
                act += 1
                scene = 0
            if ('SCENE ' + transform_alabo2_roman_num(scene + 1)) in line:
                scene += 1
                docID += 1
                sql = 'insert into docid(id,name,act,scene) value(%d,"%s",%d,%d)' % (
                    docID, child, act, scene)
                try:
                    cursor.execute(sql)
                    db.commit()
                    print("success: " + sql)
                except BaseException as e:
                    #print (e)
                    db.rollback()
                    print(sql + ";")
    db.close()
        

if __name__ == '__main__':
    filePath = 'Shakespeare'
    pathDir = os.listdir(filePath)
    # createDocID()

    # db = pymysql.connect('localhost', 'liz', 'qwer123', 'irdb')
    punctuation = {'\'s', '(', ')', ',', '.', '!', ':',
                   ';', '?', '--', '?', '\''}

    dict = {}
    docID = 0
    for allDir in pathDir:
        child = os.path.join(allDir)
        act = 0
        scene = 0
        for line in fileinput.input(filePath + '/' + child):
            if line.strip() == 'ACT ' + transform_alabo2_roman_num(act + 1):
                act += 1
                scene = 0
                continue
            if 'SCENE ' + transform_alabo2_roman_num(scene + 1) in line:
                scene += 1
                docID += 1
            for pun in punctuation:
                if pun in line:
                    line.replace(pun, ' ')
            for word in line.split():
                if word not in dict:
                    dict[word] = []
                if docID not in dict[word]:
                    dict[word].append(docID)
    json_str = json.dumps(dict)
    f = open('dictJSON.json','w')
    f.write(json_str)
    f.close()
    #print(len(dict))                        
        
