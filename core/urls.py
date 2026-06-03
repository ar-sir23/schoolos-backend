from django.urls import path
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>SchoolOS Dashboard — Coming Soon</h1>")

urlpatterns = [
    path('', home, name='home'),
]
