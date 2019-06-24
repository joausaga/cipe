from django.shortcuts import render
from app.forms import ScientistForm


def index(request):
    return render(request, 'home.html', {})


def create_scientist(request):
    form = ScientistForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = ScientistForm()
    context = {
        'form': form
    }
    return render(request, 'create.html', context)