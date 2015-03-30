from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from upload.models import Report, Report_file#, ReportForm
from django.utils import timezone
#from reports import formModels
from django import forms

LABEL_TRANSLATE = {"Author's name":"author","Report title":"title"};

# Create your views here.
def report(request):
	if request.method == 'POST':
		form = ReportForm(request.POST,request.FILES)
		if form.is_valid():
			r = Report(pub_date=timezone.now());
			#for i in (list)(form.cleaned_data.keys()):
			#	setattr(r,i,form.cleaned_data[i]);
			r.author = form.cleaned_data["author"];
			r.title = form.cleaned_data["title"];
			r.save();
			f = Report_file();
			f.file = form.cleaned_data["file"];
			f.report = r;
			f.save();
			return HttpResponse("file uploaded!");
	else:
		c = {'form':ReportForm()};
		return render(request, 'submit.html',c);
	return HttpResponse(form.is_valid());


class ReportForm(forms.Form):
	author = forms.CharField(label="Author's name", max_length = 50)
	title = forms.CharField(label="Report title", max_length = 100)
	file = forms.FileField(label="Report file");
	
def handle_uploaded_file(f,name):
    with open(name+'.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)