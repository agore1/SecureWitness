import os
import mimetypes

from django.shortcuts import render
from django.http import HttpResponse,StreamingHttpResponse
from django.core.servers.basehttp import FileWrapper
from upload.models import Report, can_view, Report_file
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.


def login(request):
    return HttpResponse("You're looking at the login page.")


# Take a report and format a few fields into a brief string
def format_report_short(report):
    report_details = ""
    report_details += 'Report id: {0} '.format(report.id)
    report_details += 'Short Description: {0} \nPublish date: {1} \nAuthor: {2}\n\n'.format(report.short_desc, report.pub_date, report.author)
    return report_details


# View to return reports based on the username, passed in from url regex
def reports(request, username=None):
    reply = ""
    # Search for all reports that are visible to this user. Reports are visible if they are:
    # Public
    public_reports = Report.objects.filter(private=False)
    # Format these into a string or list of some sort
    for report in public_reports:
        reply += "Public: " + format_report_short(report)

    # Owned by the user requesting them
    user_reports = Report.objects.filter(private=True, author=username)
    for report in user_reports:
        reply += "Owned: " + format_report_short(report)

    # Or shared to the user requesting them
    shared_reports = Report.objects.filter(can_view__user_id=request.user.id)
    for report in shared_reports:
        reply += "Shared: " + format_report_short(report)

    # Or shared to the requesting user's group
    group_shared_reports = Report.objects.filter(can_view__group__in_group__user_id=request.user.id)
    for report in group_shared_reports:
        reply += "Group shared: " + format_report_short(report)

    return HttpResponse(reply)


# Take a report and format it into a string
def format_report_long(report):
    report_details = ""
    report_details += 'Short Description: {0} \nLong Description: {1} \n'.format(report.short_desc, report.long_desc)
    report_details += 'Publish date: {0} \nAuthor: {1}\nLocation: {2} \n'.format(report.pub_date, report.author, report.location)
    return report_details


def format_files(report_id):
    """Format a string for all attached files."""
    file_details = ""
    attached_files = Report_file.objects.filter(report_id=report_id)
    if attached_files.exists():
        file_details += "The attached files are: \n"
        for file in attached_files:
            file_details += "Filenumber: " + str(file.id) + " Filename: " + str(file) + '\n'
        hint = "Execute secwit download <report id> <file number> to download attached files. "
        file_details += hint
    else:
        file_details += "No attached files."
    return file_details


# View to return a detailed report view based on the username and report id, passed in from url regex
def detailed_report(request, username=None, report_id=None):
    username = None
    if not request.user.is_authenticated():
        return HttpResponse("Sorry, you're not logged in.")
    username = request.user.username
    repId = report_id
    uId = request.user.id
    report_details = ''

    # Can view if:
    # The report is public
    report = Report.objects.filter(id=repId, private=False)
    if report.exists():
        report_details = "This report is public.\n"
        report_details += format_report_long(report[0])
        report_details += format_files(repId)
    # Current user is the owner of the report
    elif Report.objects.filter(id=repId, private=True, author=username).exists():
        report = Report.objects.filter(id=repId, private=True, author=username)
        report_details = "You are the owner of this report.\n"
        report_details += format_report_long(report[0])
        report_details += format_files(repId)
    # Or the current user has been granted permission to view it
    elif Report.objects.filter(can_view__report_id=repId, can_view__user_id=uId).exists():
        report_details = "This report has been shared with you:\n\n"
        report = Report.objects.filter(can_view__report_id=repId, can_view__user_id=uId)[0]
        report_details += format_report_long(report)
        report_details += format_files(repId)
    # Or if the current user is in a group that can view it
    elif Report.objects.filter(can_view__group__in_group__user_id = uId).exists():
        report_details = "You're in a group with access to this report:\n\n"
        report = Report.objects.filter(can_view__group__in_group__user_id=uId)[0]
        report_details += format_report_long(report)
        report_details += format_files(repId)
    else:
        report_details = "Sorry, that report either does not exist or is not visible to you."
    return HttpResponse(report_details)


def can_access(username, report_id, user_id):
    canview = False
    # Can view if:
    # The report is public
    public = Report.objects.filter(id=report_id, private=False).exists()
    # Current user is the owner of the report
    owner = Report.objects.filter(id=report_id, private=True, author=username).exists()
    # Or the current user has been granted permission to view it
    shared = Report.objects.filter(can_view__report_id=report_id, can_view__user_id=user_id).exists()
    # Or the current user is in a group with permission to view it
    groupshared = User.objects.filter(in_group__group__can_view__report_id=report_id, id=user_id).exists()
    # Reports.objects.filter((can_view__group__in_group__user_id = self.request.user.id))
    canview = public or owner or shared or groupshared
    return canview


def download_report_file(request,username=None,report_id=None,fileN=0):
    username = None
    if not request.user.is_authenticated():
        return HttpResponse("Sorry, you're not logged in.")
    # Check to make sure that the requester owns the report or has access to it.
    username = request.user.username
    repId = report_id
    uId = request.user.id
    fileNum = fileN;
    if not can_access(username, repId, uId):
        return HttpResponse("Sorry, you don't have permission to download this.")
    
    fField = Report.objects.get(id=repId).report_file_set.all()[fileNum].file
    filePath = fField.name
    fileName = os.path.basename(filePath)
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(filePath,mode='rb'),chunk_size),content_type=mimetypes.guess_type(filePath)[0])
    response['Content-Disposition'] = 'attachment; filename=%s' % fileName
    return response


def verifylogin(request, username=None):
    """Check to make sure the user successfully logged into the system."""
    if not request.user.is_authenticated() or request.user.username != username:
        return HttpResponse("False")
    else:
        return HttpResponse("True")
