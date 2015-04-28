import os
import mimetypes
import re

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
from django.db.models.query import EmptyQuerySet
from registration.models import Group
#from reports import formModels
from django import forms

class search(ListView):
    
    pDict = {};
    template_name = "search_list.html";
    reports = Report
    queryList = [];
    
    def get_context_data(self, **kwargs):
        con = super(search, self).get_context_data(**kwargs);
        con["user_name"] = self.request.user.username;
        
        return con;
    
    def get_queryset(self):
        
    
        final_list = self.reports.objects.none();
        
        for pDict in self.queryList:
            object_list = self.reports.objects.filter(private=False);
            private_list = self.reports.objects.filter(Q(can_view__user = self.request.user.id)|Q(can_view__group__in_group__user_id = self.request.user.id)|Q(author=self.request.user.username));
            filterArgs = {};
            for k in list(pDict.keys()):
                if pDict[k] != '':
                    if k == "tags":
                        tags = pDict[k].split("+");
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
                        
                        filterArgs[k] = pDict[k].replace('+',' ');
            #return(filterArgs.keys())
            object_list = object_list.filter(**filterArgs);
            private_list = private_list.filter(**filterArgs);
            object_list = list(chain(private_list,object_list));
            final_list = set(chain(final_list,object_list));
        
        return final_list;
    
    def get(self, request, *args, **kwargs):
        self.queryList = [];
        s = self.kwargs.get('slug','');
        queries = s.split("OR");
        
        for query in queries:
            if(query != ""):
                params = query.split("%");
                pDict = {};
                for p in params:
                    if p != '':
                        keyVal = p.split("-");
                        pDict[keyVal[0]] = keyVal[1];
                self.queryList.append(pDict);
        #o_list = self.get_queryset()
        return super(search, self).get(request, *args, **kwargs);

class see_report(ListView):
    template_name = "report_view.html";
    
    report = Report;
    users = User;
    groups = Group;
    viewKeys = can_view;
    
    def post(self, request, *args, **kwargs):
        postDict = request.POST.dict();
        rId = self.kwargs.get('report','');
        
        #If the user name field isn't empty, and the action selected is to add
        if(postDict["user_permission"] != '' and postDict["action"] == "Add"):
            #Create can_view() entry that relates the user and report
            uName = postDict["user_permission"];
            if(postDict["entity"] == "user"):
                userQuery = self.users.objects.filter(username=uName);
                if userQuery:
                    uId = userQuery.all()[0].id;
                    if(len(self.viewKeys.objects.filter(user=uId,report=rId).all()) < 1):
                        viewKey = can_view();
                        viewKey.user = self.users.objects.filter(username=uName).all()[0];
                        viewKey.report = self.report.objects.filter(id=rId).all()[0];
                        viewKey.save();
            elif(postDict["entity"] == "group"):
                groupQuery = self.groups.objects.filter(name=uName);
                if groupQuery:
                    gId = groupQuery.all()[0].id;
                    if(len(self.viewKeys.objects.filter(group=gId,report=rId).all()) < 1):
                        viewKey = can_view();
                        viewKey.group = self.groups.objects.get(id=gId);
                        viewKey.report = self.report.objects.filter(id=rId).all()[0];
                        viewKey.save();
        #if the action selected is to remove...
        elif(postDict["action"] == "Remove"):
            if(postDict["entity"] == "user" and list(postDict.keys()).count("user_removed") > 0):
                uName = postDict["user_removed"];
                uId = self.users.objects.get(username=uName);
                viewKey = self.viewKeys.objects.get(user_id=uId,report=rId);
                viewKey.delete();
            elif(postDict["entity"] == "group" and list(postDict.keys()).count("group_removed") > 0):
                gName = postDict["group_removed"];
                gId = self.groups.objects.get(name=gName);
                viewKey = self.viewKeys.objects.get(group_id=gId,report=rId);
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
            if(self.users.objects.filter(Q(can_view__report_id=repId,id=uId) | Q(in_group__group__can_view__report_id=repId,id=uId)).exists()):
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
            con['group_permissions'] = self.groups.objects.filter(can_view__report_id=self.kwargs.get('report',''));
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
            r.event_date = form.cleaned_data["time"];
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
        query = request.POST;
        rep.short_desc = query['short_descIn'];
        rep.long_desc = query['long_descIn'];
        rep.location = query['locationIn'];
        if list(query.keys()).count('privateIn') > 0:
            rep.private = True;
        else:
            rep.private = False;
        for i in rep.report_keyword_set.all():
            i.delete();
        tags = query['tags'].split(" ");
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
        query = request.POST;
        querySets = [];
        for k in list(request.POST.keys()):
            regex = re.search("\d+",k)
            if(regex != None):
                queryNumber = int(re.search("\d+",k).group(0));
                if(queryNumber >= len(querySets)):
                    while(len(querySets) <= queryNumber):
                        querySets.append({});
                querySets[queryNumber][re.search("\D+",k).group(0)] = request.POST[k];

        finalQuery = "";
        #return HttpResponse(querySets)
        for query in querySets:
            authorQuery = "author__{0}-{1}%".format(query["author"],query["authorIn"]);
            if query["authorIn"] == "":
                authorQuery = "";
            tagQuery = "tags-{0}%".format(query["tags"].replace(" ","+"));
            if query["tags"] == "":
                tagQuery = "";
            shortQuery = "short_desc__{0}-{1}%".format(query["short_desc"],query["short_descIn"]);
            if query["short_descIn"] == "":
                shortQuery = "";
            longQuery = "long_desc__{0}-{1}%".format(query["long_desc"],query["long_descIn"]);
            if query["long_descIn"] == "":
                longQuery = "";
            locQuery = "location__{0}-{1}".format(query["location"],query["locationIn"]);
            if query["locationIn"] == "":
                locQuery = "";
            if(finalQuery != ""):
                finalQuery += "OR";
            finalQuery += authorQuery+tagQuery+shortQuery+longQuery+locQuery;
        
        return(redirect("/upload/search="+finalQuery));
    
    c = {"user_name":request.user.username};
    
    return render(request, 'search_form.html',c);
    
#Form model
class ReportForm(forms.Form):
    short_des = forms.CharField(label="Short description", max_length = 50);
    long_des = forms.CharField(label="Long description", max_length = 500);
    time = forms.DateTimeField(label="Date of the event (Format YYYY-MM-DD, optional)", required=False);
    location = forms.CharField(label="Location (optional)", max_length = 50,required=False);
    private = forms.BooleanField(label="Private", required=False);
    tags = forms.CharField(label="Keywords (separated with commas, optional)", max_length = 100, required=False);
    
    #file = forms.FileField(label="Report file", required=False);
    
#Unused file upload method, before the use of formModels.
def handle_uploaded_file(f,name):
    with open(name+'.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
