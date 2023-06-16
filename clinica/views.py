import calendar
from datetime import datetime

import pytz as pytz
from django.shortcuts import render
from django.views import View

from clinica.forms import PacienteForm, RelatorioForm
from clinica.models import Clinica
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, DetailView, TemplateView
from paciente.models import Paciente
from paciente.views import Render


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


class MesView(TemplateView):
    template_name = 'clinica/mes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ano_atual = datetime.now().year
        meses_do_ano = []
        for mes in range(1, 13):
            data = datetime(ano_atual, mes, 1)
            nome_mes = data.strftime('%B')  # Obter o nome do mês
            meses_do_ano.append(nome_mes)
        context["meses"] = meses_do_ano
        return context


class RelatorioView(View):
    form_class = RelatorioForm
    template_name = 'clinica/relatorio.html'

    def get(self, request, id):
        clinica = Clinica.objects.get(pk=id)
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'clinica': clinica})

    def post(self, request, id):
        form = self.form_class(request.POST)
        try:
            if form.is_valid():
                data_inicial = datetime.strptime('%s 00:00:00' % form.data.get('data_inicial'), '%Y-%m-%d %H:%M:%S')
                data_final = datetime.strptime('%s 23:59:00' % form.data.get('data_final'), '%Y-%m-%d %H:%M:%S')
                datainicial = datetime(data_inicial.year, data_inicial.month, data_inicial.day,
                                       tzinfo=pytz.timezone('America/Sao_Paulo'))
                datafinal = datetime(data_final.year, data_final.month, data_final.day,
                                     tzinfo=pytz.timezone('America/Sao_Paulo'))
                if datainicial > datafinal:
                    raise Exception('Data invalida')
                clinica = Clinica.objects.get(id=id)
                pacientes = Paciente.objects.filter(clinica=clinica,
                                                    criado_em__range=(datainicial, datafinal)).order_by(
                    'criado_em')
                if len(pacientes) == 0:
                    raise Exception("Nenhum paciente encontrado entre %s e %s. Pesquise outras datas." % (
                        datainicial.date().strftime("%d/%m/%Y"), datafinal.date().strftime("%d/%m/%Y")))
                nome_arquivo = '%s%s' % (clinica.nome.replace(' ', ''), datafinal.month)
                params = {
                    'clinica': clinica,
                    'inicial': datainicial.date().strftime("%d/%m/%Y"),
                    'final': datafinal.date().strftime("%d/%m/%Y"),
                    'pacientes': pacientes,
                    'request': request,
                }
                return Render.render('paciente/relatorio.html', params, nome_arquivo)
        except Exception as e:
            return render(request, self.template_name, {'erro': str(e)})
        # return render(request, self.template_name, {'form': form})
