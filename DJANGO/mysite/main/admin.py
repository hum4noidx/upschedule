from django.contrib import admin

from .models import Discipline, Teacher, Schedule, Profile


class LessonAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['lsn_name']}),
    ]


class ScheduleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['lsn_number', 'lsn_date', 'lsn_text', 'lsn_class', 'teacher', 'lsn_grade',
                           'lsn_profile',
                           'lsn_math']}),

    ]
    list_display = ('lsn_number', 'lsn_text', 'lsn_class', 'teacher', 'lsn_date')
    list_filter = ['lsn_grade', 'lsn_profile', 'lsn_math', 'lsn_date', 'teacher']
    search_fields = ['lsn_text', 'teacher']
    ordering = ('lsn_number',)


class TeacherAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'specialization']}),

    ]
    list_display = ('name', 'specialization')
    list_filter = ['specialization']
    search_fields = ['name']


class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['profile', 'profile_db', 'grade']}),
    ]
    list_display = ('profile', 'profile_db', 'grade')
    list_filter = ['profile', 'grade']
    search_fields = ['profile']


admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Discipline, LessonAdmin)
admin.site.register(Profile, ProfileAdmin)
