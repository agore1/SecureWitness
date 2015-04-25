from django.shortcuts import render
from django.http import HttpResponse
from upload.models import Report
from django.contrib.auth.models import User

# Create your views here.


def login(request):
    return HttpResponse("You're looking at the login page.")


# View to return reports based on the username, passed in from url regex
def reports(request, username=None):
    # Search for all reports that are visible to this uer
    # Format these into a string or list of some sort

    return HttpResponse(username)


# View to return a detailed report view based on the username and report id, passed in from url regex
def detailed_report(request, username=None, report_id=None):
    username = None
    if not request.user.is_authenticated():
        return HttpResponse("Sorry, you're not logged in.")
    username = request.user.username
    repId = report_id
    uId = request.user.id
    report_details = 'Sorry, that report either does not exist or is not visible to you.'

    # Can view if:
    # The report is public
    report = Report.objects.filter(id=repId, private=False)
    if report.exists():
        report_details = report

    # Current user is the owner of the report
    elif Report.objects.filter(id=repId, private=True, author=username).exists():
        report_details = Report.objects.filter(id=repId, private=True, author=username)

    # Or the current user has been granted permission to view it
    elif Report.objects.filter(can_view__report_id=repId, id=uId).exists:
        # TODO: Change the report object
        pass
    '''
    if owner == request.user.username:
        report_list = Report.objects.filter(author=owner, id=repId)
    else:
        if User.objects.filter(can_view__report_id=repId, id=uId).exists():
            report_list = Report.objects.filter(author=owner, id=repId)
        else:
            report_list = Report.objects.filter(author=owner, id=repId, private=False)
    '''
    return HttpResponse(report_details)

