import os
import mimetypes

from itertools import chain

from django.shortcuts import render, redirect
from django.http import HttpResponse,StreamingHttpResponse
from django.template import RequestContext, loader
from upload.models import Report, Report_file, Report_keyword, Folder, can_view#, ReportForm
from django.utils import timezone
from django.views.generic.list import ListView
from django.core.files.storage import default_storage, File
from django.core.servers.basehttp import FileWrapper
from django.contrib.auth.models import User
from django.db.models import Q
#from reports import formModels
from django import forms

class search(ListView):
    
    pDict = {};
    template_name = "search_list.html";
    reports = Report
    
    def get_context_data(self, **kwargs):
        con = super(search, self).get_context_data(**kwargs);
        con["user_name"] = self.request.user.username;
        
        return con;
    
    def get_queryset(self):
        object_list = self.reports.objects.filter(private=False);
        private_list = self.reports.objects.filter(can_view__user = self.request.user.id);
        filterArgs = {};
        for k in list(self.pDict.keys()):
            if self.pDict[k] != '':
                if k == "tags":
                    tags = self.pDict[k].split("+");
                    #object_list = object_list.filter(report_keyword__keyword__in=tags);
                    #private_list = private_list.filter(report_keyword__keyword__in=tags);
                    filterArgs['report_keyword__keyword__in'] = tags;
                else:
                    '''
                    filterArgs = 
                    exec("object_list = object_list.filter("+k+"=self.pDict[k])");
                    exec("private_list = private_list.filter("+k+"=self.pDict[k])");
                    return(object_list);
                    '''
                    
                    filterArgs[k] = self.pDict[k].replace('+',' ');
        #return(filterArgs.keys())
        object_list = object_list.filter(**filterArgs);
        private_list = private_list.filter(**filterArgs);
        object_list = chain(private_list,object_list);
        
        return object_list;
    
    def get(self, request, *args, **kwargs):
        s = self.kwargs.get('slug','');
        params = s.split("%");
        self.pDict = {};
        for p in params:
            keyVal = p.split("-");
            self.pDict[keyVal[0]] = keyVal[1];
        #o_list = self.get_queryset()
        #return HttpResponse(o_list);
        return super(search, self).get(request, *args, **kwargs);

class see_report(ListView):
    template_name = "report_view.html";
    
    report = Report;
    users = User;
    viewKeys = can_view;
    
    def post(self, request, *args, **kwargs):
        postDict = request.POST.dict();
        rId = self.kwargs.get('report','');
        
        #If the user name field isn't empty, and the action selected is to add
        if(postDict["user_permission"] != '' and postDict["action"] == "Add"):
            #Create can_view() entry that relates the user and report
            uName = postDict["user_permission"];
            uId = self.users.objects.filter(username=uName).all()[0].id;
            if(len(self.viewKeys.objects.filter(user_id=uId,id=rId).all()) < 1):
                viewKey = can_view();
                viewKey.user = self.users.objects.filter(username=uName).all()[0];
                viewKey.report = self.report.objects.filter(id=rId).all()[0];
                viewKey.save();
        #if the action selected is to remove...
        elif(postDict["action"] == "Remove"):
            uName = postDict["user_removed"];
            uId = self.users.objects.get(username=uName);
            viewKey = self.viewKeys.objects.get(user_id=uId,report=rId);
            viewKey.delete();
        return redirect("/report/"+request.user.username+"/"+rId);
    
    def get(self, request, *args, **kwargs):
        owner = self.kwargs.get('user','');
        rId = self.kwargs.get('report','');
        '''
        if(owner == "Curlystraw"):
            fField = self.report.objects.get(id=rId).report_file_set.all()[0].file;
            filePath = self.report.objects.get(id=rId).report_file_set.all()[0].file.name;
            fileName = os.path.basename(filePath);
            chunk_size = 8192;
            response = StreamingHttpResponse(FileWrapper(open(filePath,mode='rb'),chunk_size),content_type=mimetypes.guess_type(filePath)[0]);
            response['Content-Disposition'] = 'attachment; filename=%s' % fileName;
            #return HttpResponse(response.reason_phrase);
            return response;
        '''
        return super(see_report, self).get(request, *args, **kwargs);
    def get_queryset(self):
        owner = self.kwargs.get('user','');#).all()[0];
        repId = self.kwargs.get('report','');
        uId = self.request.user.id;
        if(owner == self.request.user.username):
            object_list = self.report.objects.filter(author=owner,id=repId);
        else:
            if(self.users.objects.filter(can_view__report_id=repId,id=uId).exists()):
                object_list = self.report.objects.filter(author=owner,id=repId);
            else:
                object_list = self.report.objects.filter(author=owner,id=repId,private=False);
        return object_list;
    
    def get_context_data(self, **kwargs):
        con = super(see_report, self).get_context_data(**kwargs);
        con['owner_name'] = self.kwargs.get('user',None);
        #if self.request.method == "POST":
        #    con["user_name"] = "delete";
        con['editable'] = False;
        con["user_name"] = self.request.user.username;
        if(con["owner_name"] == self.request.user.username):
            con['editable'] = True;
            con['user_permissions'] = self.users.objects.filter(can_view__report_id=self.kwargs.get('report',''));
        #con['folders'] = self.folder.objects.filter(author=self.request.user.username);
        #con['folder'] = self.kwargs.get('fold',None);
        return con
    
# Create your views here.
def report(request):
    #redirect if there is no logged in user
    if request.user.is_authenticated() == False:
        return redirect("/accounts/login/");

    #if the request is a post, attempt to submit the form
    if request.method == 'POST':
        form = ReportForm(request.POST,request.FILES)
        if form.is_valid():
            rootFormQuery = Folder.objects.filter(author=request.user.username,name="ROOT");
            if(len(rootFormQuery) < 1):
                rootForm = Folder();
                rootForm.author = request.user.username;
                rootForm.name = "ROOT"
                rootForm.save();
            else:
                rootForm = rootFormQuery.all()[0];
            r = Report(pub_date=timezone.now());
            
            #I should probably make this a loop or something
            r.author = request.user.username;#User.objects.filter(username=request.user.username).all()[0];
            r.short_desc = form.cleaned_data["short_des"];
            r.long_desc = form.cleaned_data["long_des"];
            r.location = form.cleaned_data["location"];
            r.private = form.cleaned_data["private"];
            r.in_folder = rootForm;
            r.save();
            
            #Create tags
            tags = form.cleaned_data["tags"].split(" ");
            for i in tags:
                if len(i) <= 20 and i != "":
                    k = Report_keyword();
                    k.keyword = i.lstrip();
                    k.report = r;
                    k.save();
            
            #Create file object
            for file in list(request.FILES.keys()):
                f = Report_file();
                f.report = r;
                #f.file = form.cleaned_data["file"];
                f.file = request.FILES[file];
                f.save();
            return redirect("/accounts/"+request.user.username+"/reports");
    #If it's not a post, build the form
    else:
        c = {'form':ReportForm(),"user_name":request.user.username};
        return render(request, 'submit.html',c);
    return HttpResponse(form.is_valid());

def edit_form(request, report=None, user=None):
    rep = Report.objects.get(id=report);
    if(request.user.username != user):
        return redirect("/report/"+user+"/"+report);
    if request.method == 'POST':
        postData = request.POST;
        rep.short_desc = postData['short_descIn'];
        rep.long_desc = postData['long_descIn'];
        rep.location = postData['locationIn'];
        if list(postData.keys()).count('privateIn') > 0:
            rep.private = True;
        else:
            rep.private = False;
        for i in rep.report_keyword_set.all():
            i.delete();
        tags = postData['tags'].split(" ");
        for i in tags:
            if len(i) <= 20 and i != "":
                k = Report_keyword();
                k.keyword = i.lstrip();
                k.report = rep;
                k.save();
        rep.save();
        return redirect("/report/"+user+"/"+report);
    
    c = {"user_name":request.user.username};
    c['shortD'] = rep.short_desc;
    tagList = "";
    for i in rep.report_keyword_set.all():
        tagList += i.keyword+" ";
    c['tags'] = tagList;
    c['longD'] = rep.long_desc;
    c['loc'] = rep.location;
    c['private'] = rep.private;
    return render(request, 'report_edit.html',c);
    
def search_form(request):
    if request.method == 'POST':
        postData = request.POST;
        authorQuery = "author__{0}-{1}".format(postData["author"],postData["authorIn"]);
        tagQuery = "tags-{0}".format(postData["tags"].replace(" ","+"));
        shortQuery = "short_desc__{0}-{1}".format(postData["short_desc"],postData["short_descIn"]);
        longQuery = "long_desc__{0}-{1}".format(postData["long_desc"],postData["long_descIn"]);
        locQuery = "location__{0}-{1}".format(postData["location"],postData["locationIn"]);
        return(redirect("/upload/search="+authorQuery+"%"+tagQuery+"%"+shortQuery+"%"+longQuery+"%"+locQuery));
    
    c = {"user_name":request.user.username};
    
    return render(request, 'search_form.html',c);
    
#Form model
class ReportForm(forms.Form):
	short_des = forms.CharField(label="Short description", max_length = 50);
	long_des = forms.CharField(label="Long description", max_length = 500);
	location = forms.CharField(label="Location (optional)", max_length = 50,required=False);
	private = forms.BooleanField(label="Private", required=False);
	tags = forms.CharField(label="Keywords (separated with commas)", max_length = 100, required=False);
	
	#file = forms.FileField(label="Report file", required=False);
	
#Unused file upload method, before the use of formModels.
def handle_uploaded_file(f,name):
    with open(name+'.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
