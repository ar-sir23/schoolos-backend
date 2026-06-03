from django.db import models
from django.contrib.auth.models import User

class AcademicYear(models.Model):
    name       = models.CharField(max_length=20, unique=True)
    start_date = models.DateField()
    end_date   = models.DateField()
    is_current = models.BooleanField(default=False)
    def __str__(self): return self.name

class Grade(models.Model):
    name  = models.CharField(max_length=50)
    order = models.IntegerField(default=0)
    class Meta: ordering = ['order']
    def __str__(self): return self.name

class Section(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='sections')
    name  = models.CharField(max_length=10)
    class Meta: unique_together = ('grade', 'name')
    def __str__(self): return f'{self.grade.name} — {self.name}'

class Parent(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name       = models.CharField(max_length=150)
    phone      = models.CharField(max_length=20)
    email      = models.EmailField(blank=True)
    address    = models.TextField(blank=True)
    def __str__(self): return self.name

class Student(models.Model):
    GENDER_CHOICES = [('M','Male'),('F','Female'),('O','Other')]
    student_id     = models.CharField(max_length=20, unique=True)
    full_name      = models.CharField(max_length=150)
    gender         = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth  = models.DateField()
    photo          = models.ImageField(upload_to='student_photos/', blank=True)
    grade          = models.ForeignKey(Grade,        on_delete=models.SET_NULL, null=True)
    section        = models.ForeignKey(Section,      on_delete=models.SET_NULL, null=True)
    academic_year  = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, null=True)
    roll_number    = models.CharField(max_length=10, blank=True)
    parent         = models.ForeignKey(Parent, on_delete=models.SET_NULL, null=True, related_name='children')
    is_active      = models.BooleanField(default=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['grade__order', 'full_name']
    def __str__(self): return f'{self.full_name} ({self.student_id})'

    @property
    def current_attendance_rate(self):
        from management.models import Attendance
        records = Attendance.objects.filter(student=self)
        if not records.exists(): return 100.0
        present = records.filter(status='present').count()
        return round((present / records.count()) * 100, 1)
