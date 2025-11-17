from django.shortcuts import render

# Create your views here.
def home(request): 
    return render(request,'index.html')


def trying(request):
    return render(request,'go.html')