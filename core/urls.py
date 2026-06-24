from django.urls import path
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>SchoolOS — AI Powered School Management</h1>")

urlpatterns = [
    path('', home, name='home'),
]
