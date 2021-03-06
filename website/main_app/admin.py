from django.contrib import admin

from .models import Discipline, Teacher, Schedule, Passport, Material, School, Grade, Profile


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
    list_display = ('lsn_date', 'lsn_number', 'lsn_text', 'lsn_class', 'teacher',)
    ordering = ['lsn_date', 'lsn_number']
    list_filter = ['lsn_grade', 'lsn_profile', 'lsn_math', 'lsn_date', 'teacher']
    search_fields = ['lsn_text', 'teacher']


class TeacherAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'specialization', 'school']}),

    ]
    list_display = ('name', 'specialization', 'school')
    list_filter = ['specialization']
    search_fields = ['name']


class PassportAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user_id', 'uses', 'full_name', 'user_class', 'user_prof', 'vip', 'admin',
                           'registered', 'last_seen']}),
    ]
    list_display = (
        'id', 'user_id', 'full_name', 'user_class', 'user_prof', 'user_math', 'vip', 'admin', 'registered', 'last_seen')
    list_filter = ['user_class', ]
    search_fields = ['full_name']


class MaterialAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'text', 'url', 'type', 'tag', ]}),
    ]
    list_display = ('title', 'type', 'tag')
    list_filter = ['type', 'tag', ]
    search_fields = ['title', ]


class SchoolAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'city', 'short_name', ]}),
    ]
    list_display = ('id', 'name', 'city',)
    list_filter = ['city', ]
    search_fields = ['name', ]


class GradeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['grade', 'school', 'grade_short', ]}),
    ]
    list_display = ('grade', 'school',)
    list_filter = ['grade', 'school', ]
    search_fields = ['grade', ]


class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['grade', 'profile', 'math', 'profile_db', ]}),
    ]
    list_display = ('id', 'grade', 'profile',)
    list_filter = ['grade', ]
    search_fields = ['profile', ]


class MathAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['math', ]}),
    ]
    list_display = ('math',)
    list_filter = ['math', ]
    search_fields = ['math', ]


class ClassroomAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['number', 'school']}),
    ]
    list_display = ('id', 'number', 'school')
    list_filter = ['number', 'school']
    search_fields = ['number', 'school']
    sortable_by = ['id']


admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Discipline, LessonAdmin)
admin.site.register(Passport, PassportAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Profile, ProfileAdmin)
