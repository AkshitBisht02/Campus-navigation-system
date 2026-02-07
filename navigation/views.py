from django . shortcuts import render,redirect
from django.http import JsonResponse
from .models import Node
from .services import dijkstra
# Create your views here.

def landing(request):                                          # for rendering landing page (landing.html)
    return render(request,'landing.html')

def index(request):                                            # for rendering main map page (index.html)
    return render(request,'index.html')



def get_buildings(request):                                    # get buildings node to add to the map
    buildings = Node.objects.filter(type="Building").values(
        "name", "latitude", "longitude"
    )
    return JsonResponse(list(buildings), safe=False)

def get_path(request):                                          # calls A* algo for start and end point
    start = request.GET.get("start")
    end = request.GET.get("end")

    path, distance, time = dijkstra(start, end)

    return JsonResponse({
        "path": path,
        "distance": distance,
        "time": time
    })
