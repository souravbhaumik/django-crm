from django.shortcuts import redirect, render, reverse
from agents.forms import AgentModelForm
import random

from leads.models import Agent, Lead
from django.views import generic
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent

from functools import wraps
import time
# Create your views here.


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


class AgentListView(LoginRequiredMixin, generic.ListView):
    template_name = 'agent-list.html'
    context_object_name = 'agents'

    def get_queryset(self):
        return Agent.objects.filter(organisation=self.request.user.userprofile)


class AgentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Agent
    template_name = 'agent-single.html'
    context_object_name = 'agent_here'
    queryset = Agent.objects.all()


class AgentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Agent
    form_class = AgentModelForm
    template_name = "agent-create.html"

    def get_success_url(self):
        return reverse('agents:agents-all')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organiser = False
        user.set_password(str(random.randint(1, 10000)))
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile
        )
        try:
            send_mail(
                subject="You are invited to be an agent.",
                message="Agent added. Please come and start working.",
                from_email='admin@test.com',
                recipient_list=[user.email]
            )
        except:
            pass
        return super(AgentCreateView, self).form_valid(form)


class AgentUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Agent
    form_class = AgentModelForm
    template_name = "agent-update.html"
    queryset = Agent.objects.all()

    def get_success_url(self):
        return reverse('agents:agents-all')


class AgentDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "agent-delete.html"
    context_object_name = 'agent'

    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_queryset(self):
        return Agent.objects.filter(organisation=self.request.user.userprofile)
