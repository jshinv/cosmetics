from django.shortcuts import render
from django.http import HttpResponse
from common.templates.cjmall.crawling import get_data

def index(request):
    return render(
        request, 'cjmall/index.html', { } )

def datas(request):
    return render(
        request, 'cjmall/datas.html', { } )

def crawling(request):
    get_data()