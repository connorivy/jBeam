from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from .models import *
from .forms import *

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

        left_rxn = 0 
        right_rxn = 0
        for load in point_loads:
            print(load)
            new_left, new_right = load.getReactionsFromSinglePointLoad()
            left_rxn += new_left
            right_rxn += new_right

        return JsonResponse({"left_rxn": left_rxn,"right_rxn": right_rxn}, status = 200)
    return JsonResponse({}, status = 400)