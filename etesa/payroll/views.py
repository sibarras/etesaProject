from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'payroll/index.html')

def history(request):
    return render(request, 'payroll/history.html')

def new(request):
    return render(request, 'payroll/new.html')