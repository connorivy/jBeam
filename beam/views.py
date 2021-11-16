from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *
from .diagrams import Beam, PointLoad


def configure(request):
    if request.method == 'POST':
        form = addPointLoad(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('dashboard-employees')
    else:
        form = addPointLoad()

    context = {
        'form': form,
        'point_loads': pointLoad.objects.all(),
    }
    return render(request, 'beam/sidebar.html', context)


