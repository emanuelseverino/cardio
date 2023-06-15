import calendar
from datetime import datetime

import pytz as pytz

from clinica.forms import PacienteForm
from clinica.models import Clinica
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, DetailView
from paciente.models import Paciente


class ClinicaDetailView(DetailView):
    model = Clinica
    context_object_name = 'clinica'


class ClinicaNovaView(CreateView):
    model = Clinica
    fields = ['nome', ]
    success_url = '/clinica'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class ClinicaListView(ListView):
    model = Clinica
    context_object_name = 'clinicas'


class ClinicaDeleteView(DeleteView):
    model = Clinica
    success_url = '/'


class PacienteNovoView(CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'clinica/paciente_novo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clinica = Clinica.objects.get(id=self.kwargs['clinica_id'])
        ano = timezone.now().year
        mes = timezone.now().month
        primeiro_dia = datetime(ano, mes, 1, tzinfo=pytz.timezone('America/Sao_Paulo'))
        ultimo_dia = datetime(ano, mes, calendar.monthrange(ano, mes)[1], tzinfo=pytz.timezone('America/Sao_Paulo'))
        print(primeiro_dia, ultimo_dia)
        context["hoje"] = timezone.now()
        context["mes"] = timezone.now().month
        context["clinica"] = clinica
        context["pacientes"] = Paciente.objects.filter(clinica=clinica, criado_em__date=timezone.now())
        context["pacientes_mes"] = Paciente.objects.filter(clinica=clinica, criado_em__range=(primeiro_dia, ultimo_dia))
        return context

    def form_valid(self, form):
        clinica = Clinica.objects.get(id=self.kwargs['clinica_id'])
        usuario = self.request.user
        form.instance.clinica = clinica
        form.instance.usuario = usuario
        return super().form_valid(form)

    def get_success_url(self):
        clinica = self.kwargs['clinica_id']
        return f'/clinica/{clinica}/paciente/novo'
