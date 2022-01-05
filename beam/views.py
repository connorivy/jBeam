from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *


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
        'distributed_loads': distributedLoad.objects.all(),
        'beam_object': jBeamObject.objects.first(),
    }
    return render(request, 'beam/pagetables.html', context)


