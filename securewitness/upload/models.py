from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

import os
# Create your models here.


#This function sets up the upload_to field of the report_file files.
def file_path_maker(instance, f_name):
	return "/".join(['report_files',instance.report.author,f_name]);

def delete_report(report):
	for k in report.report_keyword_set.all():
		k.delete();
	for f in report.report_file_set.all():
		file = f.file;
		if(os.path.isfile(file.path)):
			os.remove(file.path);
		f.delete();
	report.delete();
	
def dupe_report(report):
	for k in report.report_keyword_set.all():
		k.delete();
	for f in report.report_file_set.all():
		file = f.file;
		if(os.path.isfile(file.path)):
			os.remove(file.path);
		f.delete();
	
def delete_folder(folder):
	for r in folder.report_set.all():
		delete_report(r);
	for f in folder.folder_set.all():
		delete_folder(f);
	folder.delete();
	
	

class can_view(models.Model):
	user = models.ForeignKey(User);
	report = models.ForeignKey('Report', default = -1);

#Model for the main report, what is there to say
class Report(models.Model):
	pub_date = models.DateTimeField('date published');
	author = models.CharField(max_length=200,default="Anonymous");
	short_desc = models.CharField(max_length = 50, default="None");
	long_desc = models.CharField(max_length=500, default = "None");
	location = models.CharField(max_length=50, default = "None");
	private = models.BooleanField(default=False);
	in_folder = models.ForeignKey('Folder', default=-1);
	def __str__(self):
		return "published on: "+str(self.pub_date);

class Folder(models.Model):
	author = models.CharField(max_length=200,default="Anonymous");
	name = models.CharField(max_length=30,default="New Folder");
	in_folder = models.ForeignKey('Folder', default = -1);
	def __str__(self):
		return self.author + " -- " + self.name;
		
#Model for report files, only includes a reference to the parent report and the file right now
#Uploads files to ROOT/report_files/<username>/<filename>
class Report_file(models.Model):
	report = models.ForeignKey(Report);
	file = models.FileField(upload_to=file_path_maker);
	def __str__(self):
		return self.filename();
	def filename(self):
		return os.path.basename(self.file.name);
		
class Report_keyword(models.Model):
	report = models.ForeignKey(Report);
	keyword = models.CharField(max_length = 20);
	def __str__(self):
		return self.keyword;
	

#Unused model for report fields, it was simpler to make the main fields of the report part of the report object.
class Report_field(models.Model):
	report = models.ForeignKey(Report);
	txt = models.CharField(max_length=200);
	ans = models.CharField(max_length=200);

