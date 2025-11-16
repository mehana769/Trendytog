from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator,EmptyPage,InvalidPage


#from trendytog.home.models import Category, Product
from home.models import Category,Product
# Create your views here.
def home(request):
    #return HttpResponse("Hello")
    return render(request,'home.html')
#def add(request):
 #   val2= int(request.POST['num2'])
  #  res=val1+val2
   # return render(request,'result.html',{'result':res})

def allprodcat(request, c_slug=None):
    c_page=None
    products=None
    if c_slug != None:
        c_page=get_object_or_404(Category,slug=c_slug)
        products_list=Product.objects.filter(category=c_page,available=True)
    else:
        products_list=Product.objects.all().filter(available=True)
    paginator=Paginator(products_list, 6)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1
    try:
        products=paginator.page(page)
    except (EmptyPage,InvalidPage):
        products=paginator.page(paginator.num_pages)
  
    return render(request,'category.html',{'Category':c_page,'products':products})


def prodetail(request,c_slug,product_slug):
    try:
        #product=Product.objects.get(category_slug=c_slug,slug=product_slug)
        product = Product.objects.get(category__slug=c_slug, slug=product_slug)

    except Exception as e:
        raise e
    #return render(request,'product.html',{'products':product})
    return render(request,'product.html',{'product':product})
