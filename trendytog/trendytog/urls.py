
# from django.urls import include, path

# from django.contrib import admin
# from django.conf.urls.static import static
# from django.conf import settings
# urlpatterns = [
#     path('accounts/', include('accounts.urls')),
#     path('admin/',admin.site.urls),
#     path('search/',include('search.urls')),
#     path('',include('home.urls')),
#     path('cart/',include('cart.urls')),
# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)







from django.urls import include, path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('cart/', include('cart.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('search/', include('search.urls')),

    # cart should be ABOVE home urls


    # home should be last
    path('', include('home.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
