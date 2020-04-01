from django.http import Http404
from django.shortcuts import render

from .models import Barist


# Create your views here.


def baristas(request):
    baristas_list = Barist.objects.all()
    return render(request, 'cafe/baristas.html', {"baristas": baristas_list})


def barista_detail(request, barista_ipn):
    try:
        barist = Barist.objects.get(ipn=barista_ipn)
    except:
        raise Http404("Barist not found")
    return render(request, 'cafe/barista.html', {"barista": barist})


def index(request):
    return render(request, 'cafe/index.html')
