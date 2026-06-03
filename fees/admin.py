from django.contrib import admin
from .models import FeeType, FeeStructure, FeeInvoice, FeePayment

admin.site.register(FeeType)
admin.site.register(FeeStructure)

@admin.register(FeeInvoice)
class FeeInvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_no','student','amount_due','amount_paid','status','ai_risk_label']
    list_filter  = ['status','ai_risk_label']

admin.site.register(FeePayment)
