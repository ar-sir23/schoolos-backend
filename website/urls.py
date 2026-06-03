from django.urls import path
from django.http import HttpResponse

def landing(request):
    return HttpResponse("<h1>SchoolOS — AI-Powered School Management</h1><p>Public site coming soon.</p>")

urlpatterns = [
    path('', landing, name='landing'),
]
