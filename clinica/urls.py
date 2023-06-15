from clinica.views import PacienteNovoView, ClinicaNovaView
from django.contrib import admin
from django.urls import path

from core.views import IndexView

urlpatterns = [
    path('nova', ClinicaNovaView.as_view(), name='clinica_novo'),
    path('<int:clinica_id>/paciente/novo', PacienteNovoView.as_view(), name='paciente_novo'),
]
