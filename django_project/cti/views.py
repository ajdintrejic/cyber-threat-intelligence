from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import Count
from .forms import UploadFileForm, EditProfileForm
from cti.models import IP
from cti.models import Log_line
from .models import Apache_log
from .log_analyzer import analyze
import threading
import os
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def home(request):
    # Get top countries by IP
    TopCountriesByIP = IP.objects.values('countryname').annotate(c=Count('countryname')).order_by('-c')[:10]
    # Number of IPs
    numberOfIPs = IP.objects.count()
    # Number of Requests
    numberOfRequests = Log_line.objects.count()
    # Number of Files
    numberOfFiles = Apache_log.objects.count()
    print(numberOfRequests)
    return render(request, 'cti/home.html', {'TopCountriesByIP': TopCountriesByIP, 'numberOfIPs': numberOfIPs, 'numberOfRequests': numberOfRequests, 'numberOfFiles': numberOfFiles})

@login_required
def uploaded_files(request):
    file_list = Apache_log.objects.all()
    path="media"
    return render(request, 'cti/uploaded_files.html', {'files': file_list})

@login_required
def search_ip(request):
    query = request.GET.get('searchInput') 
    # TODO: make a switch for every option then repeat query code based on that
    
    if (query != None):
        requestTag = request.GET.get('searchCategory')
        if (requestTag =='ipAddress'):
            ips = IP.objects.filter(address__contains=query)
            
        elif (requestTag =='countryCode'):
            ips = IP.objects.filter(country__contains=query)

        elif (requestTag =='countryName'):
            ips = IP.objects.filter(countryname__contains=query)

        elif (requestTag =='hostname'):
            ips = IP.objects.filter(hostname__contains=query)

        elif (requestTag =='city'):
            ips = IP.objects.filter(city__contains=query)

        elif (requestTag =='region'):
            ips = IP.objects.filter(region__contains=query)

        elif (requestTag =='org'):
            ips = IP.objects.filter(org__contains=query)

        elif (requestTag =='postal'):
            ips = IP.objects.filter(postal__contains=query)

        elif (requestTag =='timezone'):
            ips = IP.objects.filter(timezone__contains=query)
              

    else:
        ips = None

    path="search/ip"
    return render(request, 'cti/search_ips.html', {'ips': ips})


@login_required
def upload(request):
    if request.method == 'GET':
        return render(request, 'cti/upload.html')
    elif request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = Apache_log(log_file=request.FILES['file'])
            instance.save()
            analyzeThread = threading.Thread(target=analyze, args=(instance.log_file,))
            analyzeThread.start()

            messages.success(request, 'File is saved.')
        else:
            messages.warning(request, 'An error has occured.')
    else:
        form = UploadFileForm()
    return render(request, 'cti/upload.html', {'form': form})

@login_required
def settings(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('cti-profile'))
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'cti/settings.html', args)

@login_required
def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'cti/profile.html', args)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('cti-profile'))
        else:
            return redirect(reverse('cti-changepassword'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'cti/change_password.html', args)