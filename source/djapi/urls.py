from django.contrib import admin
# from django.conf.urls import include, url
from django.urls import include, path

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('myapi/', include('autoticketsys.urls')),
]
