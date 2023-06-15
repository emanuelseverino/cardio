from django.urls import path
from paciente.views import PacienteDeleteView, PDF, CSV, EXCEL

urlpatterns = [
    path('<int:pk>/apagar', PacienteDeleteView.as_view(), name='paciente_delete'),
    path('relatorio_pdf/<int:id>', PDF.as_view(), name='relatorio_pdf'),
    path('relatorio_csv', CSV.as_view(), name='relatorio_csv'),
    path('relatorio_excel', EXCEL.as_view(), name='relatorio_excel'),
]
