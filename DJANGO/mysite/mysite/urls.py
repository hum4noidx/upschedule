from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include(('main.urls', 'main'), namespace='main')),
    path('timetables/', include('TEST.urls')),
    path('admin/', admin.site.urls),
]
