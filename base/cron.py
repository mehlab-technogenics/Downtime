import requests, sys
from datetime import datetime,timezone
from .models import Profile, Website, History ,webData
from django.db.models import Max
from django.core.mail import send_mail,EmailMessage



def my_job():
    temp=webData.objects.all()
    sys.stdout.write('Start Job\n')
    for i in temp:
        if(i.monitored==True):
            sys.stdout.write('Ist check%s\n' %i)
            now = datetime.now(timezone.utc)
            pTime=History.objects.filter(webData=i)
            sys.stdout.write('2st check%s\n' %pTime.count())
            if(pTime.count()>0):
                tTime=pTime.latest('timestamp')
                this_time_yesterday = now - tTime.timestamp
                sys.stdout.write('2st check%s\n' %i)
                if(this_time_yesterday.total_seconds()>=((i.timePeriod*60)-(i.timePeriod*2))):
                    sys.stdout.write('2nd check%s\n' %i)
                    try:
                        temp=Website.objects.filter(id=(i.website.id)).first()
                        url=temp.url
                        r = requests.head(url)
                        a=History(websData=i,statusCode=r.status_code)
                        a.save()
                        sys.stdout.write(str('mehlaab  '+str(a)+'  '+str(a.timestamp)+'  '+str(i))+'  '+str(this_time_yesterday.total_seconds())+'\n')
                        #sys.stdout.write('mehlab is %s\n' %a.title)
                        email = EmailMessage('Hello', 'World', to=['muhammad.mehlab@technogenics.io'])
                       # email.send()
                        sys.stdout.write(str('done'+'\n'))
                    except:
                        a=History(webData=i,statusCode=0)
                       # a.save()
                        email = EmailMessage('Hello', 'Your website is down', to=['user@gmail.com'])
                        email.send()
                        sys.stdout.write(str('mehlab  '+str(a)+'  '+str(a.timestamp)+'  '+str(i))+'  '+str(this_time_yesterday.total_seconds())+'\n')
                        #sys.stdout.write('mehlab is %s\n' %a.title)
                        sys.stdout.write(str('except'+'\n'))

            else:
                url=Website.objects.filter(id=(i.website.id)).first().url
                r = requests.head(url)
                a=History(webData=i,statusCode=r.status_code)
                a.save()
                sys.stdout.write(str('mehlaab  '+str(a)+'  '+str(a.timestamp)+'  '+str(i))+'  '+'\n')



def my_scheduled_job():
    temp=webData.objects.filter(monitored=True).distinct('website')
    for i in temp:
        web=Website.objects.get(id=i.website.id)
        url=web.url
        allWebs=webData.objects.filter(website=web,monitored=True)
        print(allWebs)
        check=True
        res=None
        print(url)
        for j in allWebs:
            print(url)
            now = datetime.now(timezone.utc)
            print('\n')
            
            #print(len(pTime))
            sCode=0
            try:
                pTime=History.objects.filter(webData=j).latest('timestamp')
                this_time_yesterday = now - pTime.timestamp
                print(this_time_yesterday)
                if(this_time_yesterday.total_seconds()>=((j.timePeriod*60)-(j.timePeriod*2))):
                    print('Adding')
                    if(check==True):
                        try:
                            res=requests.get(url)
                            sCode=res.status_code
                            print(sCode)
                        except:
                            sCode=404
                        check=False
                    a=History(webData=j,statusCode=sCode)
                    a.save()
                    if(sCode!=200):
                        ema=Profile.objects.get(id=j.profile.id).email
                        print(ema)
                        send_mail('Website Down','Hi Your website is down with the url '+url+' and status Code is '+str(sCode),'raomehlab@gmail.com',[ema],fail_silently=False)
                    #email = EmailMessage('Hello', 'World', to=['muhammad.mehlab@technogenics.io'])
                    #print(email)
                    sys.stdout.write(str('mehlaab  '+str(a)+'  '+str(a.timestamp)+'  '+str(j))+'  '+'\n')
            except:
                try:
                    res=requests.get(url)
                    sCode=res.status_code
                except:
                    sCode=404
                if(sCode!=200):
                    ema=Profile.objects.get(id=j.profile.id).email
                    print(ema)
                    send_mail('Website Down','Hi Your website is down with the url '+url+' and status Code is '+str(sCode),'raomehlab@gmail.com',[ema],fail_silently=False)
                a=History(webData=j,statusCode=sCode)
                a.save()
                sys.stdout.write(str('mehlaab  '+str(a)+'  '+str(a.timestamp)+'  '+str(j))+'  '+'\n \n')



