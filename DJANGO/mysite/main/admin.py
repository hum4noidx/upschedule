from django.contrib import admin

from .models import Discipline, Teacher, Schedule, Passport, Material, School, Profile, Grade, Math, Classroom


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
        (None, {'fields': ['user_id', 'uses', 'full_name', 'user_class', 'user_prof', 'user_math', 'vip', 'admin',
                           'registered']}),
    ]
    list_display = ('id', 'user_id', 'full_name', 'user_class', 'user_prof', 'user_math', 'vip', 'admin', 'registered')
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
        (None, {'fields': ['grade', 'school', 'short_name', ]}),
    ]
    list_display = ('grade', 'school',)
    list_filter = ['grade', 'school', ]
    search_fields = ['grade', ]


class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['grade', 'profile', 'profile_db', ]}),
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


class ModelOptions(admin.ModelAdmin):
    fieldsets = (
        ('', {
            'fields': ('title', 'subtitle', 'slug', 'pub_date', 'status',),
        }),
        ('Flags', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('flag_front', 'flag_sticky', 'flag_allow_comments', 'flag_comments_closed',),
        }),
        ('Tags', {
            'classes': ('grp-collapse grp-open',),
            'fields': ('tags',),
        }),
    )


class StackedItemInline(admin.StackedInline):
    classes = ('grp-collapse grp-open',)


class TabularItemInline(admin.TabularInline):
    classes = ('grp-collapse grp-open',)


# admin.site.register(Question, QuestionAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Discipline, LessonAdmin)
admin.site.register(Passport, PassportAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Math, MathAdmin)
admin.site.register(Classroom, ClassroomAdmin)
