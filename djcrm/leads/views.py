from django.shortcuts import render

from leads.models import Lead

# Create your views here.


def home(request):
    leads = Lead.objects.all()
    context = {
        'leads': leads,
    }
    return render(request, 'home.html', context)


def lead_detail(request, pk):
    print(pk)
    context = {
    }
    return render(request, 'lead-single.html', context)
