from django.contrib import admin


# class ChoiceInline(admin.StackedInline):
#     model = Choice
#     extra = 3
#
#
# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None, {'fields': ['question_text']}),
#         ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
#     ]
#     inlines = [ChoiceInline]
#     list_display = ('question_text', 'pub_date', 'was_published_recently')
#     list_filter = ['pub_date']
#     search_fields = ['question_text']
class LessonAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['lesson_name']}),
    ]


class TimetableAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['lesson_number', 'lesson_date', 'lesson_text', 'classroom', 'teacher', 'lesson_grade',
                           'lesson_profile',
                           'lesson_math']}),

    ]
    list_display = ('lesson_number', 'lesson_text', 'classroom', 'teacher', 'lesson_date')
    list_filter = ['lesson_grade', 'lesson_profile', 'lesson_math', 'lesson_date', 'teacher']
    search_fields = ['lesson_text', 'teacher']


class TeacherAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'specialization']}),

    ]
    list_display = ('name', 'specialization')
    list_filter = ['specialization']
    search_fields = ['name']

# admin.site.register(Question, QuestionAdmin)
# admin.site.register(Timetable, TimetableAdmin)
# admin.site.register(Lecturer, TeacherAdmin)
# admin.site.register(Lesson, LessonAdmin)
