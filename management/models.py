from django.db import models
from django.contrib.auth.models import User
from core.models import Student, Grade, Section, AcademicYear

class Teacher(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    phone       = models.CharField(max_length=20, blank=True)
    department  = models.CharField(max_length=100, blank=True)
    joining_date = models.DateField()
    is_active   = models.BooleanField(default=True)
    def __str__(self): return self.user.get_full_name()

class Subject(models.Model):
    name       = models.CharField(max_length=100)
    code       = models.CharField(max_length=20, unique=True)
    grade      = models.ForeignKey(Grade, on_delete=models.CASCADE)
    teacher    = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    full_marks = models.IntegerField(default=100)
    pass_marks = models.IntegerField(default=33)
    def __str__(self): return f'{self.code} — {self.name}'

class Attendance(models.Model):
    STATUS_CHOICES = [('present','Present'),('absent','Absent'),('late','Late'),('excused','Excused')]
    student   = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    date      = models.DateField()
    status    = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    note      = models.CharField(max_length=200, blank=True)
    marked_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: unique_together = ('student', 'date'); ordering = ['-date']
    def __str__(self): return f'{self.student.full_name} — {self.date} — {self.status}'

class ExamResult(models.Model):
    EXAM_CHOICES = [('midterm','Mid Term'),('final','Final Term'),('unit','Unit Test')]
    student        = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    subject        = models.ForeignKey(Subject, on_delete=models.CASCADE)
    academic_year  = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    exam_type      = models.CharField(max_length=10, choices=EXAM_CHOICES)
    marks_obtained = models.DecimalField(max_digits=6, decimal_places=2)
    full_marks     = models.IntegerField(default=100)
    grade_letter   = models.CharField(max_length=5, blank=True)
    remarks        = models.TextField(blank=True)
    class Meta: unique_together = ('student','subject','academic_year','exam_type')

    @property
    def percentage(self): return round((float(self.marks_obtained)/self.full_marks)*100,1)

    def compute_grade_letter(self):
        p = self.percentage
        if p>=80: return 'A+'
        if p>=70: return 'A'
        if p>=60: return 'B'
        if p>=50: return 'C'
        if p>=33: return 'D'
        return 'F'

    def save(self, *args, **kwargs):
        self.grade_letter = self.compute_grade_letter()
        super().save(*args, **kwargs)
