from django.shortcuts import render
from django.http import HttpResponseRedirect
from app.forms import RegistrationForm


def index(request):
    context = {
        'lat': 41.389633,
        'lon': 2.116217
    }
    return render(request, 'index.html', context)


def registration(request):
    form = RegistrationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            print(form.cleaned_data)
            print("Formulario válido!")
            #form.save()
            return HttpResponseRedirect('/')
    context = {
        'form': form
    }
    return render(request, 'register.html', context)


def success_registration(request):
    return render(request, 'success.html')


def map_scientists(request):
    context = {
        'lat': 41.389633,
        'lon': 2.116217
    }
    return render(request, 'map.html', context)