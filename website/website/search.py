# from django.shortcuts import render
# from django.views.decorators import csrf

# def search_post(request):
#     ctx = {}
#     if request.POST:
#         ctx['rlt'] = request.POST['q']
#     return render(request, "base.html", ctx)

from django.shortcuts import render,HttpResponse
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt
import  json

@csrf_exempt
def search_post(request):
    ctx = {}
    if request.method =='POST':
        word=request.POST.get('q')
        print(word)
        ctx['rlt'] = 'asdfsafsaf'
    return render(request,'base.html',ctx)