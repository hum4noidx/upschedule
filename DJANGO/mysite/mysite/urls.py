from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(r'grappelli/', include('grappelli.urls')),
    path('', include(('main.urls', 'main'), namespace='main')),
    path('admin/', admin.site.urls),

]
