from django.shortcuts import render,HttpResponse
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from . import IRproj

@csrf_exempt
def search_post(request):
    ctx = {'rlt':'123'}
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
            tmp = IRproj.searchWord(word)
            ctx['rlt'] = tmp
        except BaseException as e:
            return HttpResponse(json.dumps({'a': 'FoundWordException!'}), content_type="application/json")
        #ctx['rlt'] = word
    return HttpResponse(json.dumps(ctx), content_type="application/json")