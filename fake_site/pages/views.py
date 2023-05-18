import datetime
import json

from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Page


# Create your views here.
@csrf_exempt
def index(request, pagename):
    request_data = request.GET or request.POST

    hackers_requests = {
        'User Agent': request.META.get('HTTP_USER_AGENT'),
        'Remote IP': request.META.get('REMOTE_ADDR'),
        'Remote Hostname': request.META.get('REMOTE_HOST'),
        'HTTP Host Header': request.META.get('HTTP_HOST'),
        'Query String': request.META.get('QUERY_STRING'),
        'Request Method': request.method,
        'Datetime of request': datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
        'Request data': request_data,
    }

    with open("hackers_info.json", "a+") as hackers_info_json:
        json.dump(hackers_requests, hackers_info_json)
        hackers_info_json.write("\n")

    pagename = "/" + pagename
    pg = get_object_or_404(Page, permalink=pagename)
    context = {
        "title": pg.title,
        "content": pg.bodytext,
        "last_updated": pg.update_date,
        "page_list": Page.objects.all(),
    }
    return render(request, "pages/page.html", context)
