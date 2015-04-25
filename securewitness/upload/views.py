import os
import mimetypes

from django.shortcuts import render, redirect
from django.http import HttpResponse,StreamingHttpResponse
from django.template import RequestContext, loader
from upload.models import Report, Report_file, Report_keyword, Folder, can_view#, ReportForm
from django.utils import timezone
from django.views.generic.list import ListView
from django.core.files.storage import default_storage, File
from django.core.servers.basehttp import FileWrapper
from django.contrib.auth.models import User
#from reports import formModels
from django import forms

def search(request, slug):
	

	return HttpResponse(slug);

class see_report(ListView):
	template_name = "report_view.html";
	
	report = Report;
	users = User;
	viewKeys = can_view;
	
	def post(self, request, *args, **kwargs):
		postDict = request.POST.dict();
		rId = self.kwargs.get('report','');
		if(list(postDict.keys()).count("user_permission") > 0):
			uName = postDict["user_permission"];
			uId = self.users.objects.filter(username=uName).all()[0].id;
			if(len(self.viewKeys.objects.filter(user_id=uId,id=rId).all()) < 1):
				viewKey = can_view();
				viewKey.user = self.users.objects.filter(username=uName).all()[0];
				viewKey.report = self.report.objects.filter(id=rId).all()[0];
				viewKey.save();
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
		con['user_name'] = self.kwargs.get('user',None);
		#if self.request.method == "POST":
		#	con["user_name"] = "delete";
		con['editable'] = False;
		if(con["user_name"] == self.request.user.username):
			con['editable'] = True;
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
			tags = form.cleaned_data["tags"].split(",");
			for i in tags:
				if len(i) <= 20 and i != "":
					k = Report_keyword();
					k.keyword = i.lstrip();
					k.report = r;
					k.save();
			
			#Create file object
			f = Report_file();
			f.report = r;
			f.file = form.cleaned_data["file"];
			f.save();
			return redirect("/accounts/"+request.user.username+"/reports");
	#If it's not a post, build the form
	else:
		c = {'form':ReportForm()};
		return render(request, 'submit.html',c);
	return HttpResponse(form.is_valid());

#Form model
class ReportForm(forms.Form):
	short_des = forms.CharField(label="Short description", max_length = 50);
	long_des = forms.CharField(label="Long description", max_length = 500);
	location = forms.CharField(label="Location (optional)", max_length = 50,required=False);
	private = forms.BooleanField(label="Private", required=False);
	tags = forms.CharField(label="Keywords (separated with commas)", max_length = 100, required=False);
	
	file = forms.FileField(label="Report file");
	
#Unused file upload method, before the use of formModels.
def handle_uploaded_file(f,name):
    with open(name+'.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)