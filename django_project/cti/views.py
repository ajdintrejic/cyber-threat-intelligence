from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import UploadFileForm, AddressForm
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
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            try:
                data = IP.objects.get(address=address)
                template = get_template('cti/viewReport.html')
                context = {
                    "ip_address" : data.address,
                    "ip_hostname" : data.hostname,
                    "ip_city" : data.city,
                    "ip_region" : data.region,
                    "ip_country" : data.countryname,
                    "ip_postal" : data.postal,
                    "ip_timezone" : data.timezone,
                    "ip_longitude" : data.longitude,
                    "ip_latitude" : data.latitude,
                    "ip_org" : data.org,
                }

                html = template.render(context)
                if 'html' in request.POST:
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
    else:
        form = AddressForm()
    return render(request, 'cti/report.html', {'form' : form})