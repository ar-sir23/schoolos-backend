from django.contrib import admin
from .models import Teacher, Subject, Attendance, ExamResult

admin.site.register(Teacher)
admin.site.register(Subject)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'status']
    list_filter  = ['status', 'date']

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'exam_type', 'marks_obtained', 'grade_letter']
