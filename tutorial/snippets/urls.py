from django.urls import path
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('snippets/', views.snippet_list, name='snippet_list'),
    path('snippets/<int:pk>/', views.snippet_detail, name='snippet_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)