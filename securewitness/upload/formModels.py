from django import forms

class ReportForm(forms.Form):
	author_name = forms.CharField(label="Author's name", max_length = 50)
	report_name = forms.CharField(label="Report title", max_length = 100)