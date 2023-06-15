from clinica.views import PacienteNovoView, ClinicaNovaView, ClinicaDeleteView, ClinicaListView, ClinicaDetailView
from django.urls import path

from core.views import IndexView

urlpatterns = [
    path('', ClinicaListView.as_view(), name='clinica_lista'),
    path('<int:pk>', ClinicaDetailView.as_view(), name='clinica_detail'),
    path('nova', ClinicaNovaView.as_view(), name='clinica_novo'),
    path('<int:clinica_id>/paciente/novo', PacienteNovoView.as_view(), name='paciente_novo'),
    path('<int:pk>/apagar', ClinicaDeleteView.as_view(), name='clinica_delete'),
]
