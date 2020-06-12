from django.urls import path
from detimakerlab.wiki.plugins.article_dependencies import views

urlpatterns = [
    path('dependencies/', views.ListAllArticles.as_view(), name='Article dependencies'),
    path('dependencies/<int:pk>/', views.DependenciesView.as_view(), name='Article dependencies'),
]