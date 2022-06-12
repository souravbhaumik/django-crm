from django.shortcuts import redirect, render, reverse
from .forms import AssignAgentForm, CreateModelForm, CustomUserCreationForm, UpdateModelForm
from .mixins import OrganiserAndLoginRequiredMixin

from leads.models import Agent, Lead
from django.views import generic
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

from functools import wraps
import time


def timer(func):
    """helper function to estimate view execution time"""

    @wraps(func)  # used for copying func metadata
    def wrapper(*args, **kwargs):
        # record start time
        start = time.time()

        # func execution
        result = func(*args, **kwargs)

        duration = (time.time() - start) * 1000
        # output execution time to console
        print('view {} takes {:.2f} ms'.format(
            func.__name__,
            duration
        ))
        return result
    return wrapper


class LandingPageView(generic.TemplateView):
    template_name = "landing.html"


class LeadListView(LoginRequiredMixin, generic.ListView):
    model = Lead
    template_name = 'lead-home.html'
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation, agent__isnull=False)
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadListView, self).get_context_data(**kwargs)
        if user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, agent__isnull=True)
            context.update({
                "unassigned_leads": queryset,
            })
        return context


class LeadDetailView(OrganiserAndLoginRequiredMixin, generic.DetailView):
    model = Lead
    template_name = 'lead-single.html'
    context_object_name = 'lead_here'
    queryset = Lead.objects.all()


class LeadCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView):
    model = Lead
    form_class = CreateModelForm
    template_name = "lead-create.html"

    def get_success_url(self):
        return reverse('leads:leads-all')

    def form_valid(self, form):
        # TODO: Send email
        send_mail(
            subject="Your lead has successfully been created.",
            message="Go to the site to view the new lead.",
            from_email="test@email.com",
            recipient_list=['testy@email.com']
        )
        return super(LeadCreateView, self).form_valid(form)


class LeadUpdateView(OrganiserAndLoginRequiredMixin, generic.UpdateView):
    model = Lead
    form_class = UpdateModelForm
    template_name = "lead-update.html"
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse('leads:leads-all')


class LeadDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    """
        This class wants a template just to delete.
        So I want to keep the funcion based views for this specific action.
    """


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"

    def get_success_url(self):
        return reverse('login')


class AssignAgentView(OrganiserAndLoginRequiredMixin, generic.FormView):
    template_name = 'assign_agent.html'
    form_class = AssignAgentForm

    def get_success_url(self):
        return reverse('leads:leads-all')


@timer
def landing_page(request):
    return render(request, 'landing.html')


@timer
def home(request):
    leads = Lead.objects.all()
    context = {
        'leads': leads,
    }
    return render(request, 'lead-home.html', context)


@timer
def lead_detail(request, pk):
    lead_here = Lead.objects.get(id=pk)
    context = {
        'lead_here': lead_here,
    }
    return render(request, 'lead-single.html', context)


@timer
def lead_create(request):
    form = CreateModelForm()
    if request.method == 'POST':
        form = CreateModelForm(request.POST)
        if form.is_valid():
            # form.save()
            Lead.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                age=form.cleaned_data['age'],
                agent=form.cleaned_data['agent'],
            )
        return redirect('leads:home')
    context = {'form': form}
    return render(request, 'lead-create.html', context)


@timer
def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = UpdateModelForm(instance=lead)
    if request.method == 'POST':
        form = UpdateModelForm(instance=lead, data=request.POST)
        if form.is_valid():
            form.save()
        return redirect('leads:home')
    context = {
        'lead': lead,
        'form': form
    }
    return render(request, 'lead-update.html', context)


@timer
def lead_delete(request, pk):
    Lead.objects.get(id=pk).delete()
    return redirect('leads:leads-all')
