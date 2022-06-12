from django.urls import path
from . import views

app_name = 'leads'

urlpatterns = [
    path('all/', views.LeadListView.as_view(), name='leads-all'),
    path('<int:pk>', views.LeadDetailView.as_view(), name='lead-single'),
    path('create/', views.LeadCreateView.as_view(), name='create-lead'),
    path('update/<int:pk>/', views.LeadUpdateView.as_view(), name='update-lead'),
    path('delete/<int:pk>/', views.lead_delete, name='delete-lead'),
    path('<int:pk>/assign-agent/',
         views.AssignAgentView.as_view(), name='assign-agent'),
]
