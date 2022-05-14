from django.shortcuts import render
from .forms import SimpleForm
# Create your views here.

def index(request):
    form = SimpleForm()
    if request.method == 'POST':
        print(request.POST)
        form = SimpleForm(request.POST)
        
    return render(request, 'forms/index.html', {'form': form})
