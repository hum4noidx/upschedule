# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question, Timetable


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'timetables/classes.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'timetables/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'timetables/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'timetables/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('timetables:results', args=(question.id,)))


class IndexView(generic.ListView):
    template_name = 'schedule/classes.html'
    context_object_name = 'timetable_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Timetable.objects.values('lesson_grade').distinct()
        # выбираем классы со ссылками на выбор профилей


def grades(request, grade):
    timetable = Timetable.objects.values('lesson_profile', ).filter(lesson_grade=grade).distinct()
    return render(request, 'schedule/profiles.html', {'timetable_list': timetable})


def profiles(request, grade, profile):
    timetable = Timetable.objects.values('lesson_math', ).filter(lesson_profile=profile).distinct()
    return render(request, 'schedule/math.html', {'timetable_list': timetable})


def timetables(request, grade, profile):
    timetable = Timetable.objects.values('lesson_number', 'lesson_date', 'lesson_text', 'classroom').filter(
        lesson_grade=grade).filter(lesson_profile=profile)
    return render(request, 'schedule/timetable.html', {'timetable_list': timetable})


class DetailView(generic.DetailView):
    template_name = 'schedule/profiles.html'
    context_object_name = 'timetable_list'

    def get_queryset(self):
        return Timetable.objects.all().filter(lesson_grade=self.kwargs['pk']).filter(lesson_profile='it')
    # def get_object(self):
    #     grade = self.kwargs['pk']
    #     return get_object_or_404(Timetable, lesson_grade=grade)


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'timetables/results.html'


def vote(request, question_id):
    ...  # same as above, no changes needed.
# Leave the rest of the views (detail, results, vote) unchanged
