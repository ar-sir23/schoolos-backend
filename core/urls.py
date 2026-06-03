from django.urls import path
from django.http import HttpResponse, JsonResponse

def home(request):
    return HttpResponse("<h1>SchoolOS Dashboard — Coming Soon</h1>")

def students(request):
    return JsonResponse([
        {"id": 1, "name": "Test Student"}
    ], safe=False)

urlpatterns = [
    path('', home, name='home'),
    path('api/students/', students, name='students'),
]
