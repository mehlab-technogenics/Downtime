from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import requests
from .cron import my_scheduled_job,my_job
from .models import Website,History,webData,Profile
from datetime import datetime
from django.core.mail import EmailMessage,send_mail
"""
def getRes(url):
    try:
        r = requests.head(url)
        return(r.status_code)
    # prints the int of the status code. Find more at httpstatusrappers.com :)
    except requests.ConnectionError:
        return(0)
"""

def home(request):
    us=Profile.objects.all()
    profile = Website.objects.filter(owner=us[1])
    up={}
    down={}
    a=webData.objects.all()
    pTime=History.objects.filter(webData=a[0])
    print(pTime)
    my_scheduled_job()
    print(profile[0])
    print('Done')
    #my_job()
    for i in profile:
        up[i.id]= History.objects.filter(webData=(webData.objects.filter(website=i).first()),statusCode=200).count()
        h=History.objects.filter(webData=(webData.objects.filter(website=i).first())).count()
        down[i.id]=(h-up[i.id])
    
    context={'profile': profile,'up':up,'down':down}
    #print(context)
    #print('mehlab', context['history'][i.id])
    return render(request, 'home.html', context)