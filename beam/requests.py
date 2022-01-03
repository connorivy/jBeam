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
        try:
            load_type = request.POST.get('loadType')
        except:
            print('Could not retrieve load type')
            return

        if load_type == 'point':
            try:
                point_load = pointLoad.objects.get(index = index)
                point_load.startMagnitude = request.POST.get("startMagnitude", None)
                point_load.startLocation = request.POST.get("startLocation", None)
                point_load.save()
                json_response = {
                    "startMagnitude":point_load.startMagnitude,
                    "startLocation":point_load.startLocation, 
                }
            except:
                point_load = pointLoad.objects.create(index=index, startMagnitude=request.POST.get("startMagnitude", None), startLocation=request.POST.get("startLocation", None))

        elif load_type == 'distributed':
            try:
                distributed_load = distributedLoad.objects.get(index = index)
                distributed_load.startMagnitude = request.POST.get("startMagnitude", None)
                distributed_load.startLocation = request.POST.get("startLocation", None)
                distributed_load.endMagnitude = request.POST.get("endMagnitude", None)
                distributed_load.endLocation = request.POST.get("endLocation", None)
                distributed_load.save()
                json_response = {
                    "startMagnitude":distributed_load.startMagnitude,
                    "startLocation":distributed_load.startLocation,
                    "endMagnitude":distributed_load.endMagnitude,
                    "endLocation":distributed_load.endLocation, 
                }
            except:
                json_response = {
                    "startMagnitude":distributed_load.startMagnitude,
                    "startLocation":distributed_load.startLocation,
                    "endMagnitude":distributed_load.endMagnitude,
                    "endLocation":distributed_load.endLocation, 
                }
                print(json_response)
                # distributed_load = distributedLoad.objects.create(index=index, startMagnitude=request.POST.get("startMagnitude", None), startLocation=request.POST.get("startLocation", None), endMagnitude=request.POST.get("endMagnitude", None), endLocation=request.POST.get("endLocation", None))

        return JsonResponse(json_response, status = 200)
    return JsonResponse({}, status = 400)

@csrf_exempt
def update_model(request):
    if request.is_ajax and request.method == "POST":
        try:
            user_beam = jBeamObject.objects.first()
            user_beam.L = request.POST.get("L", None)
            user_beam.save()
            json_response = {
                'success': True,
            }
        except:
            json_response = {
                'success': False,
            }
        return JsonResponse(json_response, status = 200)
    return JsonResponse({}, status = 400)

def get_diagrams(request):
    if request.is_ajax and request.method == "GET":
        # # get beam from client side
        # beam = request.GET.get("beam", None)
        point_loads = pointLoad.objects.all()
        distributed_loads = distributedLoad.objects.all()
        user_beam = jBeamObject.objects.first()

        calc_beam = beam(user_beam.L, x0 = 0)
        for pl in point_loads:
            calc_beam.add_point_load(pl.startLocation, pl.startMagnitude)

        
        for dl in distributed_loads:
            m = (float(dl.endMagnitude) - float(dl.startMagnitude)) / (float(dl.endLocation) - float(dl.startLocation))
            b = float(dl.startMagnitude) - m * float(dl.startLocation)
            calc_beam.add_distributed_load(dl.startLocation, dl.endLocation, f'{m}*x + {b}')

        calc_beam.add_support(0, "roller")
        calc_beam.add_support(user_beam.L, "pin")

        calc_beam.solve()

        output = calc_beam.get_chart_values(subs={'E': (29000 * 144)})

        return JsonResponse(output, status = 200)

    return JsonResponse({}, status = 400)