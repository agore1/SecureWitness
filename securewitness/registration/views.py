"""
Views which allow users to create and activate accounts.

"""

from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import logout
from django.utils import timezone

from registration import signals
from registration.forms import RegistrationForm, loginForm
from upload.models import Report, delete_report

#def ReportEdit(request):
#	return render(request, 'submit.html', {});
	#return redirect("/accounts/"+request.user.username+"/reports");

class ReportListView(ListView):
	model = Report;
	
	slug = None;
	
	def get_object(self, queryset=None):
		return queryset.get(slug=self.slug);
	
	def get_queryset(self):
		user = self.kwargs.get('slug','');
		if(user != ''):
			if(user != self.request.user.username):
				object_list = self.model.objects.filter(author=user,private=False);
			else:
				object_list = self.model.objects.filter(author=user);
		else:
			object_list = [];
		return object_list;
	
	def get_context_data(self, **kwargs):
		con = super(ReportListView, self).get_context_data(**kwargs);
		con['user_name'] = self.kwargs.get('slug',None);
		if self.request.method == "POST":
			con["user_name"] = "delete";
		con['editable'] = False;
		if(con["user_name"] == self.request.user.username):
			con['editable'] = True;
		return con
		
	def post(self, request, *args, **kwargs):
		if(request.POST["action_taken"] == "delete"):
			for key in (list)(request.POST.keys()):
				if key[0:5] == "check":
					reportID = request.POST[key];
					report = self.model.objects.filter(id=int(reportID))[0];
					delete_report(report);
		return HttpResponse(request.POST.items());

class _RequestPassingFormView(FormView):
    """
    A version of FormView which passes extra arguments to certain
    methods, notably passing the HTTP request nearly everywhere, to
    enable finer-grained processing.

    """
    def get(self, request, *args, **kwargs):
        # Pass request to get_form_class and get_form for per-request
        # form control.
        form_class = self.get_form_class(request)
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        # Pass request to get_form_class and get_form for per-request
        # form control.
        form_class = self.get_form_class(request)
        form = self.get_form(form_class)
        if form.is_valid():
            # Pass request to form_valid.
            return self.form_valid(request, form)
        else:
            return self.form_invalid(form)

    def get_form_class(self, request=None):
        return super(_RequestPassingFormView, self).get_form_class()

    def get_form_kwargs(self, request=None, form_class=None):
        return super(_RequestPassingFormView, self).get_form_kwargs()

    def get_initial(self, request=None):
        return super(_RequestPassingFormView, self).get_initial()

    def get_success_url(self, request=None, user=None):
        # We need to be able to use the request and the new user when
        # constructing success_url.
        return super(_RequestPassingFormView, self).get_success_url()

    def form_valid(self, form, request=None):
        return super(_RequestPassingFormView, self).form_valid(form)

    def form_invalid(self, form, request=None):
        return super(_RequestPassingFormView, self).form_invalid(form)


class RegistrationView(_RequestPassingFormView):
    """
    Base class for user registration views.

    """
    disallowed_url = 'registration_disallowed'
    form_class = RegistrationForm
    http_method_names = ['get', 'post', 'head', 'options', 'trace']
    success_url = 'register/complete/'
    template_name = 'registration/registration_form.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Check that user signup is allowed before even bothering to
        dispatch or do other processing.

        """
        if not self.registration_allowed(request):
            return redirect(self.disallowed_url)
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, request, form):
        new_user = self.register(request, **form.cleaned_data)
        success_url = self.get_success_url(request, new_user)

        # success_url may be a simple string, or a tuple providing the
        # full argument set for redirect(). Attempting to unpack it
        # tells us which one it is.
        try:
            to, args, kwargs = success_url
            return redirect(to, *args, **kwargs)
        except ValueError:
            return redirect(success_url)

    def registration_allowed(self, request):
        """
        Override this to enable/disable user registration, either
        globally or on a per-request basis.

        """
        return True

    def register(self, request, **cleaned_data):
        """
        Implement user-registration logic here. Access to both the
        request and the full cleaned_data of the registration form is
        available here.

        """
        raise NotImplementedError


class ActivationView(TemplateView):
    """
    Base class for user activation views.

    """
    http_method_names = ['get']
    template_name = 'registration/activate.html'

    def get(self, request, *args, **kwargs):
        activated_user = self.activate(request, *args, **kwargs)
        if activated_user:
            success_url = self.get_success_url(request, activated_user)
            try:
                to, args, kwargs = success_url
                return redirect(to, *args, **kwargs)
            except ValueError:
                return redirect(success_url)
        return super(ActivationView, self).get(request, *args, **kwargs)

    def activate(self, request, *args, **kwargs):
        """
        Implement account-activation logic here.

        """
        raise NotImplementedError

    def get_success_url(self, request, user):
        raise NotImplementedError

def login(request):
	if request.method == 'POST':
		form = userForm(request.POST)
		if form.is_valid():
			user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password']);
			if user is not None: 
				return(HttpResponse("Logged in"));
			else:
				return HttpResponse("Username/Password combination invalid.");
	else:
		c = {'form':userForm()};
		return render(request, 'login.html',c);
	
def logout_view(request):
	logout(request);
	if request.user.is_authenticated():
		return HttpResponse("wat");
	return redirect("/accounts/login/");
	
def profile(request):
	if request.user.is_authenticated():
		c = {'user_name':request.user.username};
		return render(request, 'registration\profile.html',c);
	return redirect("/accounts/login/");
