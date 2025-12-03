from django.shortcuts import render
from gestion.models import Platillo

def menu(request):
    platillos = Platillo.objects.all()
    context = {
        'platillos': platillos
    }
    return render(request, 'restaurant/menu.html', context)
