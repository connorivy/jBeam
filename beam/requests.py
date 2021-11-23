from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from .models import *
from .forms import *
from symbeam import beam
import json

@csrf_exempt
def update_point_load(request):
    if request.is_ajax and request.method == "POST":
        # get the index from the client side.
        index = request.POST.get("index", None)

        # check for the point load in the database.
        point_load = pointLoad.objects.get(index = index)

        try:
            point_load.magnitude = request.POST.get("magnitude", None)
            point_load.location = request.POST.get("location", None)
            point_load.save()
        except:
            location = ''
            magnitude = ''
        return JsonResponse({"magnitude":point_load.magnitude,"location":point_load.location}, status = 200)
    return JsonResponse({}, status = 400)

def get_diagrams(request):
    if request.is_ajax and request.method == "GET":
        # # get beam from client side
        # beam = request.GET.get("beam", None)
        print('request')
        point_loads = pointLoad.objects.all()
        user_beam = jBeamObject.objects.first()

        calc_beam = beam(user_beam.L, x0 = -100)
        for pl in point_loads:
            print(pl.location)
            calc_beam.add_point_load(pl.location, pl.magnitude)

        calc_beam.add_support(-100, "roller")
        calc_beam.add_support(100, "pin")

        calc_beam.solve()

        output = calc_beam.get_chart_values(subs={'E': 29000})

        return JsonResponse(output, status = 200)

    return JsonResponse({}, status = 400)