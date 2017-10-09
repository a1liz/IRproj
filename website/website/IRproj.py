import os
import fileinput
import pymysql
import json


def wordRecording(filePath):
    ''' 
    将每个单词在文章中出现的次数存入json文件中
    '''
    pathDir = os.listdir(filePath)
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
                line = line.replace('SCENE ' + transform_alabo2_roman_num(scene), ' ')
            for pun in punctuation:
                if pun in line:
                    line = line.replace(pun, ' ')
            for word in line.lower().split():
                if word not in dict:
                    dict[word] = []
                if docID not in dict[word]:
                    dict[word].append(docID)
    json_str = json.dumps(dict)
    try:
        f = open('wordRecording.json', 'w')
        f.write(json_str)
        f.close()
    except BaseException as e:
        print("error: " + e)


def transform_alabo2_roman_num(one_num):
    '''
    将阿拉伯数字转化为罗马数字 
    '''
    num_list = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    str_list = ["M", "CM", "D", "CD", "C", "XC",
                "L", "XL", "X", "IX", "V", "IV", "I"]
    res = ''
    for i in range(len(num_list)):
        while one_num >= num_list[i]:
            one_num -= num_list[i]
            res += str_list[i]
    return res


def transform_roman_num2_alabo(one_str):
    '''
    将罗马数字转化为阿拉伯数字 
    '''
    define_dict = {'I': 1, 'V': 5, 'X': 10,
                   'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    if one_str == '0':
        return 0
    else:
        res = 0
        for i in range(0, len(one_str)):
            if i == 0 or define_dict[one_str[i]] <= define_dict[one_str[i - 1]]:
                res += define_dict[one_str[i]]
            else:
                res += define_dict[one_str[i]] - \
                    2 * define_dict[one_str[i - 1]]
        return res


def createDocID(filePath):
    '''
    生成docID
    '''
    pathDir = os.listdir(filePath)
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
            if ('SCENE ' + transform_alabo2_roman_num(scene + 1)) in line:
                scene += 1
                docID += 1
                dict[docID] = {}
                dict[docID]['name'] = child[0:-5]
                dict[docID]['ACT'] = transform_alabo2_roman_num(act)
                dict[docID]['SCENE'] = transform_alabo2_roman_num(scene)
    json_str = json.dumps(dict)
    try:
        f = open('docID.json', 'w')
        f.write(json_str)
        f.close()
    except BaseException as e:
        print("error: " + e)
        

if __name__ == '__main__':
    filePath = 'Shakespeare'
    wordRecording(filePath)
        
