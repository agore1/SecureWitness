from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from upload.models import Report, Report_file, Report_keyword#, ReportForm
from django.utils import timezone
#from reports import formModels
from django import forms


# Create your views here.
def report(request):
	#redirect if there is no logged in user
	if request.user.is_authenticated() == False:
		return redirect("/accounts/login/");

	#if the request is a post, attempt to submit the form
	if request.method == 'POST':
		form = ReportForm(request.POST,request.FILES)
		if form.is_valid():
			r = Report(pub_date=timezone.now());
			
			#I should probably make this a loop or something
			r.author = request.user.username;
			r.short_desc = form.cleaned_data["short_des"];
			r.long_desc = form.cleaned_data["long_des"];
			r.location = form.cleaned_data["location"];
			r.private = form.cleaned_data["private"];
			r.save();
			
			#Create tags
			tags = form.cleaned_data["tags"].split(",");
			for i in tags:
				if len(i) <= 20:
					k = Report_keyword();
					k.keyword = i.lstrip();
					k.report = r;
					k.save();
			
			#Create file object
			f = Report_file();
			f.report = r;
			f.file = form.cleaned_data["file"];
			f.save();
			return HttpResponse("file uploaded!");
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
	private = forms.BooleanField(label="Private");
	tags = forms.CharField(label="Keywords (separated with commas)", max_length = 100, required=False);
	
	file = forms.FileField(label="Report file");
	
#Unused file upload method, before the use of formModels.
def handle_uploaded_file(f,name):
    with open(name+'.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)