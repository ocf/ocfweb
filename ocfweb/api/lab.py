from django.http import JsonResponse
from ocflib.lab.stats import users_in_lab_count
from ocflib.infra.hosts import hosts_by_filter
from ocflib.lab.stats import list_desktops
from ocflib.lab.stats import get_connection

public_desktops = list_desktops(public_only = True)

def collect_desktops():
    """Collect the currently in use desktops for today."""
    with get_connection() as c:
        query = '''
            SELECT `host`
            FROM `session_duration_public`
            WHERE `duration` is NULL
        '''
        c.execute(query)
    # trimming suffix "ocf.berkeley.edu" from each host 
    desktops = {r['host'][:-17] for r in c}
    return desktops

def desktop_usage(request):
    num_desktops = len(public_desktops)

    # get the list of public-only dekstops in use
    public_desktops_inuse = collect_desktops().intersection(public_desktops) 
    
    return JsonResponse({
        "public_desktops": list(public_desktops_inuse),
        "total_desktops": num_desktops,
        })
    

