from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def login(request):
    return HttpResponse("You're looking at the login page.")


# View to return reports based on the username, passed in from url regex
def reports(request, username=None):
    # Search for all reports that are visible to this uer
    # Format these into a string or list of some sort

    return HttpResponse(username)

