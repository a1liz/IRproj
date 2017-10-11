import os
import fileinput
import json
from website import global_list


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
        
def searchWord(word):
    data = {}
    with open('website/wordRecording.json') as json_file:
    # with open('wordRecording.json') as json_file:
        data = json.load(json_file)
        wordSet = set()
        if word in data:
            for i in data[word]:
                wordSet.add(i)
    return wordSet
    # return data[word]



import re

# 将word所有括号自底向上解析出来
def searchForBracket(word,num):
    #pattern = re.compile(r'\(\w*[&\|~]*\w*\)')
    #pattern = re.compile(r'a+')
    #match = pattern.match(word)
    m = re.findall(r'\(\w*[&\|~\$]*\w*\)',word,re.M|re.I)
    for i in m:
        global_list.reDict[num] = i
        word = word.replace(i,'$'+str(num),1)
        num = num + 1
    if re.findall(r'\(\w*[&\|~\$]*\w*\)',word,re.M|re.I):
        searchForBracket(word,num)
    else:
        global_list.reDict[num] = word
    return toDocID(searchAllWord())

# 将解析后的reDict结果进行集合逻辑运算，并返回最终结果
def searchAllWord():
    num = 1

    while num in global_list.reDict:
        global_list.reDict[num] = global_list.reDict[num].replace('(','')
        global_list.reDict[num] = global_list.reDict[num].replace(')','')
        m = re.findall(r'[&\|~]',global_list.reDict[num],re.M|re.I)
        # print(m)
        if len(m) == 0:
            global_list.resultDict[num] = getWordSet(global_list.reDict[num])
        # 最简形式
        elif len(m) == 1:
            wordArray = divideWord(global_list.reDict[num])
            global_list.resultDict[num] = simpleMatch([getWordSet(wordArray[0]),wordArray[1],wordArray[2]])
        # 复杂形式
        else :
            wordArray = divideWord(global_list.reDict[num])
            global_list.resultDict[num] = complexMatch([getWordSet(wordArray[0]),wordArray[1],wordArray[2]])
        num = num + 1
    return global_list.resultDict[len(global_list.reDict)]

# 将整句分成左部、运算符、右部
def divideWord(word):
    m = re.findall(r'[&\|~]',word,re.M|re.I)
    op = m[0]
    x,y = word.split(op)
    return [x,op,y]

# 返回单词对应的docID集合
def getWordSet(word):
    if len(re.findall(r'\$[\d]+',word,re.M|re.I)) == 1:
        wordSet = global_list.resultDict[int(word.replace('$',''))]
        # print('wordSet1')
        # print(wordSet)
    else:
        wordSet = searchWord(word)
        # print('wordSet2')
        # print(wordSet)
    return wordSet


# 单一形式语句匹配结果
def simpleMatch(setAndWordArray):
    setx = setAndWordArray[0]
    op = setAndWordArray[1]
    y = setAndWordArray[2]
    sety = getWordSet(y)
    # 集合运算
    if op == '&':
        setResult = setx & sety
    elif op == '|':
        setResult = setx | sety
    elif op == '~':
        setResult = setx - sety
    return setResult

# 复杂形式语句匹配结果
def complexMatch(setAndWordArray):
    if len(re.findall(r'[&\|~]',setAndWordArray[2],re.M|re.I)) == 0:
        return simpleMatch(wordArray)
    else :
        newWordArray = divideWord(setAndWordArray[2])
        setx = simpleMatch([setAndWordArray[0],setAndWordArray[1],newWordArray[0]])
        return complexMatch([setx,newWordArray[1],newWordArray[2]])

        
def toDocID(setResult):
    arrayResult = []
    for i in setResult:
        arrayResult.append(int(i))
    arrayResult = sorted(arrayResult)
    tmpName = ""
    result = ''
    # with open('docID.json') as json_file:
    with open('website/docID.json') as json_file:
        data = json.load(json_file)
        for i in arrayResult:
            if str(i) in data:
                if tmpName != data[str(i)]['name']:
                    result += '<br/>' + data[str(i)]['name'] + ' '
                    tmpName = data[str(i)]['name']
                result += ',ACT ' + data[str(i)]['ACT'] + ' SCENE ' + data[str(i)]['SCENE']
    return result





if __name__ == '__main__':
    print(searchForBracket('judgment&(and~go)',1))
