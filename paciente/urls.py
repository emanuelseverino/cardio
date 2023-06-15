from clinica.views import PacienteNovoView
from django.contrib import admin
from django.urls import path

from core.views import IndexView
from paciente.views import PacienteDeleteView

urlpatterns = [
    path('<int:pk>/apagar', PacienteDeleteView.as_view(), name='paciente_delete'),
]
