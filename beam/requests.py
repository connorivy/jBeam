from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from .models import *
from .forms import *
from symbeam import beam

@csrf_exempt
def update_point_load(request):
    if request.is_ajax and request.method == "POST":
        # get the index from the client side.
        index = request.POST.get("index", None)

        # check for the point load in the database.
        print('getting point load')
        try:
            point_load = pointLoad.objects.get(index = index)
            point_load.magnitude = request.POST.get("magnitude", None)
            point_load.location = request.POST.get("location", None)
            point_load.save()
        except:
            point_load = pointLoad.objects.create(index=index, magnitude=request.POST.get("magnitude", None), location=request.POST.get("location", None))
        print('point load', point_load)

        try:
            user_beam = jBeamObject.objects.first()
            user_beam.L = request.POST.get("L", None)
            user_beam.save()
        except:
            location = ''
            magnitude = ''
        return JsonResponse({"magnitude":point_load.magnitude,"location":point_load.location, 'L':user_beam.L}, status = 200)
    return JsonResponse({}, status = 400)

def get_diagrams(request):
    if request.is_ajax and request.method == "GET":
        # # get beam from client side
        # beam = request.GET.get("beam", None)
        point_loads = pointLoad.objects.all()
        user_beam = jBeamObject.objects.first()

        calc_beam = beam(user_beam.L, x0 = 0)
        for pl in point_loads:
            calc_beam.add_point_load(pl.location, pl.magnitude)

        calc_beam.add_support(0, "roller")
        calc_beam.add_support(user_beam.L, "pin")

        calc_beam.solve()

        output = calc_beam.get_chart_values(subs={'E': (29000 * 144)})

        return JsonResponse(output, status = 200)

    return JsonResponse({}, status = 400)