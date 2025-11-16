from django.conf import settings
from django.urls import path
from.import views
app_name='home'

urlpatterns = [
    # path('',views.home,name='home'),
#   #  path('add/',views.add,name='add'),
   path('',views.allprodcat,name='allprodcat'),
   path('<slug:c_slug>/',views.allprodcat,name='products_by_category'),
   path('<slug:c_slug>/<slug:product_slug>/',views.prodetail,name='prodetail'),
#    path('<slug:c_slug>/<slug:product_slug>/', views.prodetail, name='prodetail'),

 ]

