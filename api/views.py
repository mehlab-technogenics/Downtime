from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from base.models import Website,webData,Profile,History
import datetime
from .serializers import Historyerializer, ProfileSerializer,WebsiteSerializer,UserSerializer
# Create your views here.


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET': '/api/Websites'},
        {'GET': '/api/My-Websites'},
        {'GET': '/api/web-history'},
        {'GET': '/api/users'},
        {'GET': '/api/credential'},
       # {'POST': '/api/projects/id/vote'},
        {'POST': '/api/register'},
        {'POST': '/api/token'},
        {'POST': '/api/token/refresh'},
        {'POST': '/api/addWebsite'},
        {'PUT': '/api/addWebsite'},
        {'DELETE': '/api/deleteWebsite'}
    ]
    return Response(routes)

@api_view(['GET'])
def getWebsites(request):
    websites = Website.objects.all()
    serializer = WebsiteSerializer(websites, many=True)
    return Response(serializer.data)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def getMyWebsites(request):
    project = Profile.objects.get(user=request.user)
    websites = Website.objects.filter(owner=project)
    serializer = WebsiteSerializer(websites, many=True)
    return Response(serializer.data)

@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def deleteWebsite(request, pk):
    try:
        project = Profile.objects.get(user=request.user)
        print(project)
        websites = Website.objects.get(id=pk)
        print(websites)
        a=webData.objects.filter(profile=project,website=websites)
        print(a)
        a.delete()
        print('Done')
        project = Profile.objects.get(user=request.user)
        websites = Website.objects.filter(owner=project)
        serializer = WebsiteSerializer(websites, many=True)
        return Response(serializer.data)
        
    except:
        print('Not Deleting')
        project = Profile.objects.get(user=request.user)
        websites = Website.objects.filter(owner=project)
        serializer = WebsiteSerializer(websites, many=True)
        return Response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def getLoguser(request):
    data=request.user
    project = Profile.objects.get(user=request.user)
    serializer = ProfileSerializer(project, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getUsers(request):
    websites = Profile.objects.all()
    print(websites)
    serializer = ProfileSerializer(websites, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getWebsite(request, pk):
    project = Website.objects.get(id=pk)
    serializer = WebsiteSerializer(project, many=False)
    return Response(serializer.data)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def getWebHistory(request, pk):
    project = Profile.objects.get(user=request.user)
    websites = Website.objects.get(id=pk)
    a=webData.objects.get(profile=project,website=websites)
    print(a)
    data=History.objects.filter(webData=a)
    print(datetime.datetime.now())
    print(data)
    serializer = Historyerializer(data, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getuserWeb(request, pk):
    project = webData.objects.get(Profile=pk)
    serializer = WebsiteSerializer(project, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def create_auth(request):
    user = User.objects.create_user(username=request.data['username'],
                                 email=request.data['email'],
                                 password=request.data['password'])
    profile=Profile.objects.create(user=user,name=request.data['username'],email=request.data['email'])
    #serializer = UserSerializer(data=request.data)
    serializer = ProfileSerializer(profile, many=False)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST','PUT'])
@permission_classes([IsAuthenticated])
def addWebsite(request):
    print(request.headers)
    data = request.data
    user=request.user
    
    entry=Website.objects.filter(url=data['url'])
    #entry = Website.objects.get(url=data['url']).exists()
    project = Profile.objects.get(user=request.user)
    mon=True
    if(data['monitored']==0 or data['monitored']==''):
        mon=False
    if(request.method == 'POST'):
        if(len(entry) == 0):
            
            a=Website(title=data['title'],email=data['email'],monitored=mon,timePeriod=data['timePeriod'],url=data['url'])
            a.save()
            a.owner.add(project)
            a.save()
            b=webData(profile=project,website=a,monitored=data['monitored'],timePeriod=data['timePeriod'])
            b.save
        else:
            a=Website.objects.get(url=data['url'])
            #b=Website.object.get(id=a.id)
            a.owner.add(project)
            a.save()
            #a.owner.add(project)
            b=webData(profile=project,website=a,monitored=data['monitored'],timePeriod=data['timePeriod'])
            b.save
    else:
        a=Website.objects.filter(id=data['id']).update(title=data['title'],email=data['email'],monitored=mon,timePeriod=data['timePeriod'],url=data['url'])
        webData.objects.filter(profile=project,website=a).update(monitored=data['monitored'],timePeriod=data['timePeriod'])
    a=Website.objects.get(url=data['url'])
    print('adding',a.url)
    serializer = WebsiteSerializer(a, many=False)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
