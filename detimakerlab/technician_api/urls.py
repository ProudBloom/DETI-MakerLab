"""makerlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from detimakerlab.technician_api import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="DETIMaker Lab API",
        default_version='v1',
        description="v1 of DETIMaker Lab API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.MainPage.as_view(), name='Main Page'),
    path('login/', views.login, name='Login'),

    path('equipments/', views.ListAllEquipments.as_view(), name='List all equipments'),
    path('equipments/<str:pk>/', views.EquipmentsDetails.as_view(), name='Equipments details'),

    path('projects/', views.ListAllProjects.as_view(), name='List all projects'),
    path('projects/<int:pk>/', views.ProjectsDetails.as_view(), name='Projects details'),

    path('students/', views.StudentsView.as_view(), name='List all students'),
    path('students/<int:pk>', views.StudentsDetailsView.as_view(), name='Students details'),

    path('groups/', views.GroupsView.as_view(), name='List all groups'),
    path('groups/<str:pk>', views.GroupsDetailsView.as_view(), name='Groups details'),

    # Requests
    path('requests/', views.ListAllRequests.as_view(), name='Requests'),
    path('requests/<str:pk>/', views.RequestsDetails.as_view(), name='Requests'),
    path('requests/approve/<str:pk>/', views.ApproveRequest.as_view(), name='Make Request'),
    path('requests/deny/<str:pk>/', views.DenyRequest.as_view(), name='Make Request'),
    path('borrow/<str:pk>/', views.BorrowEquipments.as_view(), name='Validate equipment borrow'),
    path('return/<str:pk>/', views.ReturnEquipments.as_view(), name='Validate equipment return'),

    # Exits
    path('exits/', views.ListAllExits.as_view(), name='Exits'),
    path('exits_to_project/<int:pk>', views.ExitsByProject.as_view(), name='Equipment borrowed to a project'),

    # Missing
    path('missing/', views.MissingView.as_view(), name='Missing'),
    path('missing/<int:pk>', views.MissingDetailsView.as_view(), name='EDetails of missing equipment'),

    # Documentation
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Statistics
    url('stats/', views.Statistics.as_view(), name='Statistics'),

    # Groups where a student is part of
    path('student_groups/<int:pk>/', views.StudentGroups.as_view(), name='Groups a student is part of'),
]


admin.site.site_header = "Makers Lab Admin"
admin.site.site_title = "Makers Lab Admin Portal"
admin.site.index_title = "Make's Lab Administration Page"
