"""detimakerlab URL Configuration

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
from django.conf.urls.static import static
from django.urls import path, include

from detimakerlab import design, settings

urlpatterns = [
                  # API's
                  path('wiki/', include('detimakerlab.wiki.urls')),
                  path('tech/', include('detimakerlab.technician_api.urls')),
                  # path('users/', include('detimakerlab.users_api.urls')), # Not in use
                  # path('admin/', admin.site.urls),

                  # Web pages
                  path('', design.homepage, name="homepage"),
                  path('about', design.about, name="about"),
                  path('all_equipment', design.all_equipment, name="all_equipments"),
                  path('create_project', design.create_project, name="create_project"),
                  path('navbar', design.nav_bar, name="nav_bar"),
                  path('rent_equipment', design.rent_equipment, name="rent_equipment"),
                  path('return_equipment', design.return_equipment, name="return_equipment"),
                  path('student', design.student, name="student"),
                  path('not_logged_in', design.not_logged_in, name="not_logged_in"),
                  path('login', design.login),
                  path('technician', design.technician, name="technician"),
                  path('requests', design.requests, name='requests'),
                  path('edit_equipment', design.edit_equipment, name='edit_equipment'),
                  path('statistics', design.statistics, name='statistics'),
                  path('my_projects', design.my_projects, name='my_projects'),
                  path('team', design.team, name='team'),

                  # WIKI STUFF
                  path('test/', include('detimakerlab.wiki.plugins.article_dependencies.urls'))

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
