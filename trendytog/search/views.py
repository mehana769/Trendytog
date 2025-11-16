from django.shortcuts import render
from home.models import Product
from django.db.models import Q
# Create your views here.
def searchResult(request):
    products=None
    query=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        products=Product.objects.filter(Q(name_icontains=query) | Q(description_icontains=query) | Q(categoryname_icontains=query).distinct())
    return render(request,'search.html',{'query':query,'products':products})


