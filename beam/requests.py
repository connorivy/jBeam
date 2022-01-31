from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from .models import *
from .forms import *
from symbeam import beam
from .utils import query_to_list

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
            except:
                distributed_load = distributedLoad.objects.create(index=index, startMagnitude=request.POST.get("startMagnitude", None), startLocation=request.POST.get("startLocation", None), endMagnitude=request.POST.get("endMagnitude", None), endLocation=request.POST.get("endLocation", None))

        return JsonResponse({}, status = 200)
    return JsonResponse({}, status = 400)

@csrf_exempt
def update_model(request):
    # get the index from the client side.
    type = request.POST.get('type', None)
    index = request.POST.get("index", None)
    
    json_response = {}
    if request.is_ajax and request.method == "POST":
        if type == 'support':
            try:
                update_support(index, request.POST.get("location", None))
                update_beam(request.POST.get("L", None))
                json_response = {
                    'success': True,
                }
            except:
                json_response = {
                    'success': False,
                }
        elif type == 'point':
            try:
                update_point(index, request.POST.get("startLocation", None))
                json_response = {
                    'success': True,
                }
            except:
                json_response = {
                    'success': False,
                }
        elif type == 'dist':
            try:
                update_dist(index, request.POST.get("startLocation", None), request.POST.get("endLocation", None))
                json_response = {
                    'success': True,
                }
            except:
                json_response = {
                    'success': False,
                }        
        return JsonResponse(json_response, status = 200)
    return JsonResponse({}, status = 400)

def update_support(index, location):
    sup = support.objects.get(index = index)
    sup.location = location
    sup.save()

def update_beam(L):
    user_beam = jBeamObject.objects.first()
    user_beam.L = L
    user_beam.save()

def update_point(index, startLocation):
    point_load = pointLoad.objects.get(index = index)
    point_load.startLocation = startLocation
    point_load.save()

def update_dist(index, startLocation, endLocation):
    distributed_load = distributedLoad.objects.get(index = index)
    # distributed_load.startMagnitude = request.POST.get("startMagnitude", None)
    if startLocation:
        distributed_load.startLocation = startLocation
    # distributed_load.endMagnitude = request.POST.get("endMagnitude", None)
    if endLocation:
        distributed_load.endLocation = endLocation
    distributed_load.save()


import skyciv
def get_diagrams(request):
    if request.is_ajax and request.method == "GET":
        # # get beam from client side
        # beam = request.GET.get("beam", None)
        point_loads = pointLoad.objects.all()
        distributed_loads = distributedLoad.objects.all()
        user_beam = jBeamObject.objects.first()

        try:
            skycivCalc(user_beam.L, -5, 15)
        except Exception as e:
            print(f'\nThe following error occured: {e}')
            
        
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

        output = calc_beam.get_chart_values(subs={'E': .8 * (29000 * 144)}) # multiply by .8 per AISC requirements (doesn't always apply so I need to fix this later)
        output['sections'] = query_to_list(section.objects.filter(Ixx__gt = float(output['I_req'])))

        return JsonResponse(output, status = 200)

    return JsonResponse({}, status = 400)

def skycivCalc(L, load_mag, load_loc):
    print(L, load_loc, load_mag)
    # Create an instance of the Model class
    model = skyciv.Model("imperial")

    # Nodes
    model.nodes.add(0, 0, 0)
    model.nodes.add(30, 0, 0)

    # Members
    model.members.add(1, 2, 1)

    # Sections
    model.sections.add_library_section( skyciv.sections.American_AISC_W_shapes_W14x22, 1)

    # Material
    # model.materials.add("Structural Steel")  # For metric
    model.materials.add("Structural Steel", "imperial") # For imperial
    # model.materials.add("Structural Steel", model.settings.units.get_unit_system())  # For the model's current units
    # model.materials.addCustom("Custom Steel", 7850, 210000, 0.29, 300, 440, "steel") # For custom material

    # Supports
    model.supports.add(1, "FFFFRR")
    model.supports.add(2, "FFFFRR")

    # Settlements
    # model.settlements.add(35, ty=-10)

    # Add point load
    model.point_loads.add("m", member=1, position=15, y_mag= -5, load_group="LG1")
    # model.point_loads.add("n", node=13, y_mag=1.6, load_group="LG1")
    # model.point_loads.add("n", node=12, y_mag=-3.7, load_group="LG1")

    # Add moment
    # model.moments.add("n", node=12, y_mag=0.3, load_group="LG1")
    # model.moments.add("m", member=16, position=0, x_mag=-0.1, load_group="LG1")

    # Add distributed load
    # model.distributed_loads.add(32, y_mag_A=-10, y_mag_B=-2, position_B=100, load_group="LG1")

    # Pressure
    # model.pressures.add(1, "global", 0, 0, 0.1, "LG1")

    # Area load
    # model.area_loads.add("one_way", [23, 24, 25, 26], 1.3, "Z", column_direction=[23, 26], LG="LG1")

    # Selfweight
    model.self_weight.add(y=-1, LG="SW1")

    # Make a load combination
    model.load_combinations.add("SW1 + LG1", {"SW1": 1, "LG1": 1})

    # Create an API Object
    ao = skyciv.ApiObject()

    # Set auth
    ao.auth.username = "civy@rlginc.com"
    ao.auth.key = "llBksd5Mfh0mjPAwc7PeJ2HZTMAJzeU8oqTaWj2ZhwEBw2soTMkSA1CAvNq3UtIW"

    # Set functions
    print('start')
    ao.functions.add("S3D.session.start", {"keep_open": True})
    print('set')
    ao.functions.add("S3D.model.set", {"s3d_model": model})
    # Uncomment the next line to run a solve as well.
    # print('analyse')
    ao.functions.add("S3D.model.solve", {"analysis_type": "linear"})

    ao.functions.add("S3D.design.member.optimize", {
        "design_code": "AISC_360-10_LRFD",
        "simplified": True,
        "section_height": {
            "min": 8,
            "max": 30
        },
    })
    # print('solved')
    ao.functions.add("S3D.file.save", {"name": "test", "path": "api/PIP/"})

    res = ao.request()
    print('requested')

    print(res["response"])
