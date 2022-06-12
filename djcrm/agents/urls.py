from django.urls import path
from . import views


app_name = 'agents'


urlpatterns = [
    path('', views.AgentListView.as_view(), name='agents-all'),
    path('<int:pk>/', views.AgentDetailView.as_view(), name='agent-single'),
    path('create/', views.AgentCreateView.as_view(), name='create-agent'),
    path('update/<int:pk>/', views.AgentUpdateView.as_view(), name='update-agent'),
    path('delete/<int:pk>/', views.AgentDeleteView.as_view(), name='delete-agent'),
]
