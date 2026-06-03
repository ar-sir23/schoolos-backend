from django.contrib import admin
from .models import Student, Parent, Grade, Section, AcademicYear

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display  = ['full_name', 'student_id', 'grade', 'section', 'is_active']
    list_filter   = ['grade', 'is_active', 'gender']
    search_fields = ['full_name', 'student_id']

admin.site.register(Parent)
admin.site.register(Grade)
admin.site.register(Section)
admin.site.register(AcademicYear)
