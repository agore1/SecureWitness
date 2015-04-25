import os
import mimetypes

from django.shortcuts import render
from django.http import HttpResponse,StreamingHttpResponse
from django.core.servers.basehttp import FileWrapper
from upload.models import Report, can_view, Report_file
from django.contrib.auth.models import User

# Create your views here.


def login(request):
    return HttpResponse("You're looking at the login page.")


# View to return reports based on the username, passed in from url regex
def reports(request, username=None):
    # Search for all reports that are visible to this uer
    # Format these into a string or list of some sort

    return HttpResponse(username)


# Take a report and format it into a string
def format_report(report):
    report_details = ""
    report_details += 'Short Description: {0} \nLong Description: {1} \n'.format(report.short_desc, report.long_desc)
    report_details += 'Publish date: {0} \nAuthor: {1}\nLocation: {2} \n'.format(report.pub_date, report.author, report.location)
    return report_details


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
        report_details = "This report is public."
        report_details += format_report(report[0])

    # Current user is the owner of the report
    elif Report.objects.filter(id=repId, private=True, author=username).exists():
        report = Report.objects.filter(id=repId, private=True, author=username)
        report_details = "You are the owner of this report.\n"
        report_details += format_report(report[0])

    # Or the current user has been granted permission to view it
    elif Report.objects.filter(can_view__report_id=repId, can_view__user_id=uId).exists():
        report_details = "This report has been shared with you:\n\n"
        report = Report.objects.filter(can_view__report_id=repId, can_view__user_id=uId)[0]
        report_details += format_report(report)
        attached_files = Report_file.objects.filter(report_id=repId)
        if attached_files.exists():
            report_details += "The attached files are: \n"
            for file in attached_files:
                report_details = report_details + str(file) + '\n'
        hint = "Execute secwit download <filename> <report id> to download attached files. "
        report_details += hint

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

def download_report_files(request,username=None,report_id=None,file=0):
    username = None
    if not request.user.is_authenticated():
        return HttpResponse("Sorry, you're not logged in.")
    username = request.user.username
    repId = report_id
    uId = request.user.id
    fileNum = file;
    
    
    
    fField = Report.objects.get(id=report_id).report_file_set.all()[fileNum].file
    filePath = fField.name
    fileName = os.path.basename(filePath)
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(filePath,mode='rb'),chunk_size),content_type=mimetypes.guess_type(filePath)[0])
    response['Content-Disposition'] = 'attachment; filename=%s' % fileName
    return response