from django.shortcuts import render,HttpResponse
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from . import IRproj

@csrf_exempt
def search_post(request):
    ctx = {'rlt':'实例：judgment&(and~go)'}
    if request.method =='POST':
        word=request.POST.get('q')
        ctx['rlt'] = 'afasdfasfas'
    return render(request,'base.html',ctx)


@csrf_exempt
def ajax(request):
    ctx = {'rlt':'2323'}
    if request.method =='POST':
        word=request.POST['q']
        try:
            #tmp = IRproj.searchWord(word)
            if word == " ":
                ctx['rlt'] = '请输入值'
            result = IRproj.searchForBracket(word,1)
            if result == '':
                ctx['rlt'] = '结果为空'
            else:
                ctx['rlt'] = result
        except BaseException as e:
            return HttpResponse(json.dumps({'a': 'FoundWordException!'}), content_type="application/json")
        #ctx['rlt'] = word
    return HttpResponse(json.dumps(ctx), content_type="application/json")