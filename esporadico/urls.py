from django.urls import path
from .views import (
    EsporadicoCreateView, 
    EsporadicoListView, 
    esporadico_update_view, 
    EsporadicoDeleteView
)

urlpatterns = [
    path('esporadico/', EsporadicoListView.as_view(), name='esporadico_list'),
    path('esporadico/novo/', EsporadicoCreateView.as_view(), name='esporadico_create'),
    path('esporadico/<int:pk>/editar/', esporadico_update_view, name='esporadico_update'),
    path('esporadico/<int:pk>/excluir/', EsporadicoDeleteView.as_view(), name='esporadico_delete'),
]