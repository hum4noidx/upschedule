from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
                  path('', views.index, name='index'),
                  path('about-us', views.about, name='about'),
                  path('schedule/', views.grades, name='grade'),
                  path('schedule/<int:pk>/', views.ProfileListlView.as_view(), name='profile'),
                  path('schedule/<int:pk>/<int:prof>/<str:math>/', views.days, name='days'),
                  path('schedule/<int:pk>/<int:prof>/<str:math>/<int:day>', views.schedule, name='schedule'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
