from django.urls import path

from . import views

app_name = 'timetables'
urlpatterns = [
    # path('', views.timetable, name='timetable'),
    path('', views.IndexView.as_view(), name='schedule'),
    path('<int:grade>/', views.grades, name='grade'),
    path('<int:grade>/<str:profile>/', views.profiles, name='profile'),
    path('<int:grade>/<str:profile>/show/', views.timetables, name='timetable'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:grade>/schedule/', views.vote, name='vote'),
]
