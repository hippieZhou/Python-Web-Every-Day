from django.contrib import admin

from .models import Student
# Register your models here.


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sex', 'profession', 'email',
                    'qq', 'phone', 'status', 'created_time',)
    list_filter = ('sex', 'status', 'created_time',)
    search_fields = ('name', 'profession',)
    fieldsets = (
        (None, {
            "fields": (
                'name',
                ('sex', 'profession'),
                ('email', 'qq', 'phone'),
                'status',
            ),
        }),
    )
