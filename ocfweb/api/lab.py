from django.http import JsonResponse
from ocflib.lab.stats import users_in_lab_count
from ocflib.infra.hosts import hosts_by_filter
from ocflib.lab.stats import list_desktops

def desktop_usage(request):
    num_desktops = len(list_desktops(public_only = False))
    num_users = users_in_lab_count()
    return JsonResponse({
            "users_in_lab": num_users,
            "total_desktops": num_desktops,
            })
    

