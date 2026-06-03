from django.db import models
from django.utils import timezone
from core.models import Student, Grade, AcademicYear
import random

class FeeType(models.Model):
    name         = models.CharField(max_length=100)
    is_recurring = models.BooleanField(default=True)
    def __str__(self): return self.name

class FeeStructure(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    grade         = models.ForeignKey(Grade,        on_delete=models.CASCADE)
    fee_type      = models.ForeignKey(FeeType,      on_delete=models.CASCADE)
    amount        = models.DecimalField(max_digits=10, decimal_places=2)
    due_day       = models.IntegerField(default=10)
    class Meta: unique_together = ('academic_year','grade','fee_type')
    def __str__(self): return f'{self.grade} — {self.fee_type}: ৳{self.amount}'

class FeeInvoice(models.Model):
    STATUS_CHOICES = [('pending','Pending'),('partial','Partial'),('paid','Paid'),('overdue','Overdue'),('waived','Waived')]
    student       = models.ForeignKey(Student,      on_delete=models.CASCADE, related_name='invoices')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE)
    invoice_no    = models.CharField(max_length=30, unique=True)
    amount_due    = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid   = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_date      = models.DateField()
    status        = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    ai_risk_score = models.IntegerField(default=0)
    ai_risk_label = models.CharField(max_length=10, default='low')
    created_at    = models.DateTimeField(auto_now_add=True)

    @property
    def balance_due(self): return self.amount_due - self.amount_paid

    def save(self, *args, **kwargs):
        if not self.invoice_no:
            self.invoice_no = f'INV-{timezone.now().year}-{random.randint(10000,99999)}'
        if self.amount_paid >= self.amount_due: self.status = 'paid'
        elif self.amount_paid > 0: self.status = 'partial'
        elif self.due_date < timezone.now().date() and self.status == 'pending': self.status = 'overdue'
        super().save(*args, **kwargs)

    def __str__(self): return f'{self.invoice_no} — {self.student.full_name}'

class FeePayment(models.Model):
    METHOD_CHOICES = [('cash','Cash'),('bank','Bank'),('bkash','bKash'),('nagad','Nagad'),('card','Card')]
    invoice        = models.ForeignKey(FeeInvoice, on_delete=models.CASCADE, related_name='payments')
    amount         = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=METHOD_CHOICES, default='cash')
    transaction_id = models.CharField(max_length=100, blank=True)
    paid_at        = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        inv = self.invoice
        inv.amount_paid = sum(p.amount for p in inv.payments.all())
        inv.save()
