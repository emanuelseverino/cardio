import csv
import datetime
import io
import calendar
from datetime import datetime
import pytz as pytz
from django.utils import timezone
import xlwt
from django.http import HttpResponse
from django.views import View
from django.views.generic import DeleteView

from clinica.models import Clinica
from paciente.models import Paciente
import xhtml2pdf.pisa as pisa
from django.template.loader import get_template


class PacienteDeleteView(DeleteView):
    model = Paciente

    def get_success_url(self):
        paciente = Paciente.objects.get(pk=self.kwargs['pk'])
        return '/clinica/%s/paciente/novo' % paciente.clinica.pk


class Render:
    @staticmethod
    def render(path: str, params: dict, filename: str):
        template = get_template(path)
        html = template.render(params)
        response = io.BytesIO()
        pdf = pisa.pisaDocument(
            io.BytesIO(html.encode('UTF-8')), response
        )
        if not pdf.err:
            response = HttpResponse(
                response.getvalue(), content_type='application/pdf'
            )
            response['Content-Disposition'] = 'attachment;filename=%s.pdf' % filename
            return response
        else:
            return HttpResponse('Error Renderig PDF', status=400)


class PDF(View):
    def get(self, request, id):
        clinica = Clinica.objects.get(id=id)
        hoje = timezone.now().date()
        ano = timezone.now().year
        mes = timezone.now().month
        mes_nome = calendar.month_name[timezone.now().month]
        primeiro_dia = datetime(ano, mes, 1, tzinfo=pytz.timezone('America/Sao_Paulo'))
        ultimo_dia = datetime(ano, mes, calendar.monthrange(ano, mes)[1], tzinfo=pytz.timezone('America/Sao_Paulo'))
        pacientes = Paciente.objects.filter(clinica=clinica, criado_em__range=(primeiro_dia, ultimo_dia)).order_by(
            'criado_em')
        nome_arquivo = '%s%s' % (clinica.nome.replace(' ', ''), mes_nome)
        params = {
            'clinica': clinica,
            'hoje': hoje,
            'mes': mes,
            'pacientes': pacientes,
            'request': request,
        }
        return Render.render('paciente/relatorio.html', params, nome_arquivo)


class CSV(View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="relatorios.csv"'

        pacientes = Paciente.objects.all()

        writer = csv.writer(response)
        writer.writerow(['id', 'Nome', 'Data', ])
        for paciente in pacientes:
            writer.writerow([paciente.pk, paciente.nome, paciente.criado_em, ])

        return response


class EXCEL(View):
    def get(self, request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="pacientes.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Pacientes')

        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Id', 'Nome', 'Data', ]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()

        pacientes = Paciente.objects.all()

        row_num = 1
        for paciente in pacientes:
            data = '%s' % format(paciente.criado_em, "%d/%m/%Y")
            ws.write(row_num, 0, paciente.pk, font_style)
            ws.write(row_num, 1, paciente.nome, font_style)
            ws.write(row_num, 2, data, font_style)
            row_num += 1
        wb.save(response)
        return response
