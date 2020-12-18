from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import UploadFileForm, AddressForm, StatisticsForm
from cti.models import IP, Log_line
from .models import Apache_log
from .log_analyzer import analyze
from django.template.loader import get_template
from .pdf_generator import render_to_pdf

def home(request):
    return render(request, 'cti/home.html')


@login_required
def upload(request):
    if request.method == 'GET':
        return render(request, 'cti/upload.html')
    elif request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = Apache_log(log_file=request.FILES['file'])
            instance.save()
            print(instance.log_file) #ime fajla
            analyze(instance.log_file)

            messages.success(request, 'File is saved.')
        else:
            messages.warning(request, 'An error has occured.')
    else:
        form = UploadFileForm()
    return render(request, 'cti/upload.html', {'form': form})

@login_required
def report(request):
    if request.method == 'POST':
        if 'htmlST' in request.POST or 'pdfST' in request.POST:
            form = StatisticsForm(request.POST)
        else:
            form = AddressForm(request.POST)
        if form.is_valid():
            if 'htmlST' in request.POST or 'pdfST' in request.POST:
                param = form.cleaned_data['parameter']
                value = form.cleaned_data['value']

                try:
                    if param == "Country":
                        data = IP.objects.filter(countryname=value)
                    elif param == "City":
                        data = IP.objects.filter(city=value)
                    elif param == "Region":
                        data = IP.objects.filter(region=value)
                    elif param == "Request method":
                        log_ip = Log_line.objects.filter(requestMethod=value).values_list('ip_address_id', flat=True).distinct()
                        data = IP.objects.filter(id__in=log_ip)
                    if not data:
                        raise IP.DoesNotExist
                    template = get_template('cti/statisticsReport.html')
                    context = {
                        "data" : data,
                        "parameter" : param,
                        "count" : data.count(),
                        "value" : value,
                    }

                    html = template.render(context)
                    if 'htmlST' in request.POST:
                        return HttpResponse(html)

                    pdf = render_to_pdf('cti/statisticsReport.html', context)
                    if pdf:
                        response = HttpResponse(pdf, content_type='application/pdf')
                        content = "attachment; filename='Report.pdf'"
                        download = request.GET.get("download")
                        response['Content-Disposition'] = content
                        return response
                    return HttpResponse("Not found")
                except(IP.DoesNotExist):
                    messages.warning(request, 'Invalid input.')
            else:
                address = form.cleaned_data['address']
                try:
                    data = IP.objects.get(address=address)
                    id = data.id
                    data_logs = Log_line.objects.filter(ip_address_id=id)
                    template = get_template('cti/viewReport.html')
                    context = {
                        "ip" : data,
                        "ip_log" : data_logs,
                    }

                    html = template.render(context)
                    if 'htmlIP' in request.POST:
                        return HttpResponse(html)

                    pdf = render_to_pdf('cti/viewReport.html', context)
                    if pdf:
                        response = HttpResponse(pdf, content_type='application/pdf')
                        content = "attachment; filename='Report.pdf'"
                        download = request.GET.get("download")
                        response['Content-Disposition'] = content
                        return response
                    return HttpResponse("Not found")

                except(IP.DoesNotExist):
                    messages.warning(request, 'IP address not found.')

    return render(request, 'cti/report.html', {'form' : AddressForm(), 'formST' : StatisticsForm()})