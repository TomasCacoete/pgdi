from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# vai ser usada nos urls.py
def view_test(request):
    print("Hello from view_test")
    return HttpResponse("Hello from view_test")
