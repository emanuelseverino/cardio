from django.views.generic import DeleteView
from paciente.models import Paciente


class PacienteDeleteView(DeleteView):
    model = Paciente

    def get_success_url(self):
        paciente = Paciente.objects.get(pk=self.kwargs['pk'])
        return '/clinica/%s/paciente/novo' % paciente.clinica.pk
