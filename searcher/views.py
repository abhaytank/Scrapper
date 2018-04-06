from django.shortcuts import render
from .forms import *
from crawler import *

def searchq(request):
    form = InputText(request.POST or None)
    context = { "form" : form }
    if form.is_valid():
        instance = form.save(commit=false)
        instance.save()
        query1 = instance.query
    return render(request, 'searcher/header.html' , context )
                  
def index(request):
    main_query = request.POST["query"]
    temp = main_query
    corpus1 = obj.returncorp()
    return render(request, 'searcher/index.html' ,  {'result':obj.get( temp , corpus1)} )

def about(request):
    return render(request , 'searcher/about.html' , {} )


