from django.contrib import admin

from .models import Discipline, Teacher, Schedule, Passport, Material


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


class TeacherAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'specialization']}),

    ]
    list_display = ('name', 'specialization')
    list_filter = ['specialization']
    search_fields = ['name']


class PassportAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user_id', 'uses', 'full_name', 'user_class', 'user_prof', 'user_math', 'vip', 'admin',
                           'registered']}),
    ]
    list_display = ('user_id', 'full_name', 'user_class')
    list_filter = ['user_class', ]
    search_fields = ['full_name']


class MaterialAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'text', 'url', 'type', 'tag', ]}),
    ]
    list_display = ('title', 'type', 'tag')
    list_filter = ['type', 'tag', ]
    search_fields = ['title', ]


# admin.site.register(Question, QuestionAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Discipline, LessonAdmin)
admin.site.register(Passport, PassportAdmin)
admin.site.register(Material, MaterialAdmin)
