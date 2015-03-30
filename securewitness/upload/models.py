from django.db import models
from django.forms import ModelForm
# Create your models here.

class Report(models.Model):
	pub_date = models.DateTimeField('date published');
	author = models.CharField(max_length=200,default="Anonymous");
	title = models.CharField(max_length=200,default="Untitled")
	def __str__(self):
		return "published on: "+str(self.pub_date);

class Report_file(models.Model):
	report = models.ForeignKey(Report);
	file = models.FileField();
	def __str__(self):
		return "File";

class Report_field(models.Model):
	report = models.ForeignKey(Report);
	txt = models.CharField(max_length=200);
	ans = models.CharField(max_length=200);

'''
class ReportForm(ModelForm):
	class Meta:
		model = Report;
		fields = ['author','title','file'];

'''