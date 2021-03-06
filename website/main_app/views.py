from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Grade, Profile, Schedule, Date


# №1 generates grades list from db
def grades(request):
    grades_list = Grade.objects.all().order_by('grade')
    return render(request, 'main/grade.html', {'grades': grades_list})


def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


class GradeListlView(ListView):
    model = Grade
    template_name = 'main/grade.html'
    context_object_name = 'grade'
    ordering = ['grade']


class ProfileListlView(ListView):
    model = Profile
    template_name = 'main/profile.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        return Profile.objects.values().filter(grade_id=self.kwargs['pk']).order_by('profile_db')


class Days(ListView):
    model = Date
    template_name = 'main/days.html'
    context_object_name = 'days'

    def get_queryset(self):
        return Date.objects.values('id', 'day')


def days(request, pk, prof, math):
    days_list = {
        1: 'Понедельник',
        2: 'Вторник',
        3: 'Среда',
        4: 'Четверг',
        5: 'Пятница',

    }
    profile = Profile.objects.values().filter(id=prof)
    return render(request, 'main/days.html', {'grade': pk,
                                              'profile': profile,
                                              'math': math,
                                              'days': days_list})


def schedule(request, pk, prof, math, day):
    print(pk, prof, day)
    schedule = Schedule.objects.all().filter(lsn_grade=pk).filter(lsn_profile=prof).filter(lsn_math=math).filter(
        lsn_date=day).order_by(
        'lsn_date', 'lsn_number')
    return render(request, 'main/schedule.html', {'schedule': schedule, })


class ScheduleDetailView(DetailView):
    model = Schedule
    template_name = 'main/schedule.html'
    context_object_name = 'schedule'

    def get_queryset(self):
        # return Profile.objects.all().filter(grade_id=self.kwargs['pk'])
        print(self.kwargs['pk'])
        print(self.kwargs['prof'])
        print(self.kwargs['day'])
        return
