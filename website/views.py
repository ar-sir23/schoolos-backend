from django.http import HttpResponse

def landing(request):
    return HttpResponse("<h1>SchoolOS</h1>")
