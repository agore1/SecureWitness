from django.contrib import admin
from upload.models import Report, Report_file, Report_keyword


# Register your models here.

#class FieldInline(admin.StackedInline):
#	model = Form_field;
#	extra = 1;

class FileInline(admin.StackedInline):
	model = Report_file;
	extra = 1;

class KeywordInline(admin.StackedInline):
	model = Report_keyword;
	extra = 0;
	
class ReportAdmin(admin.ModelAdmin):
	inlines = [FileInline,KeywordInline];
admin.site.register(Report, ReportAdmin);