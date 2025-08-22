from django.urls import path
from .views import (
    EsporadicoCreateView,
    EsporadicoListView,
    esporadico_update_view,
    EsporadicoDeleteView,
    atribuir_valor_view
)

urlpatterns = [
    path('esporadico/', EsporadicoListView.as_view(), name='esporadico_list'),
    path('esporadico/novo/', EsporadicoCreateView.as_view(), name='esporadico_create'),
    path('esporadico/<int:pk>/editar/', esporadico_update_view, name='esporadico_update'),
    path('esporadico/<int:pk>/excluir/', EsporadicoDeleteView.as_view(), name='esporadico_delete'),
    path('esporadico/<int:pk>/atribuir-valor/', atribuir_valor_view, name='esporadico_atribuir_valor'),
]