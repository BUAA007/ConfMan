from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from Meeting.models import Meeting
from Meeting.serializers import MeetingSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import loader


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

    def create(self, request):
        meeting_serializer=MeetingSerializer(data=request.data)
        if meeting_serializer.is_valid():
            title = request.data.get("title")
            intro = request.data.get("intro")
            essay_request = request.data.get("essay_request")
            ddl_date = request.data.get("ddl_date")
            result_notice_date = request.data.get("result_notice_date")
            regist_attend_date = request.data.get("regist_attend_date")
            meeting_date = request.data.get("meeting_date")
            meeting_end_date=request.data.get("meeting_end_date")
            schedule = request.data.get("schedule")
            if (ddl_date<=result_notice_date) and (result_notice_date<=regist_attend_date) and (regist_attend_date<=meeting_date) and (meeting_date<=meeting_end_date):
                thisMeeting = Meeting(title,intro ,essay_request,ddl_date,result_notice_date,regist_attend_date, meeting_date,meeting_end_date, schedule, )
                thisMeeting.save()
                return Response(thisMeeting.meeting_id, status=status.HTTP_201_CREATED)
            return Response("error: Meeting is not valid",status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False)
    def showdetail(self, request):
        user_id=1
        pk = request.query_params.get('pk',None)
        thisMeeting=Meeting.objects.get(meeting_id=pk)
        papers=thisMeeting.paper_set.all()
        thisuser=User.objects.get(id=user_id)
        favorite=thisuser.favorite.get(thisMeeting)
        if favorite is None:
            isfavorite = False
        else : 
            isfavorite =True
        i=0
        paper_list=list()
        serializer = MeetingSerializer(thisMeeting)
        paper_list.append(serializer.data)
        paper_info={"title":"","author":""}
        for paper in papers:
            paper_info["title"]=paper.title
            paper_info["author"]=paper.author_1
            paper_list.append(paper_info)
            i=i+1
            if i>=10:
                break
        template = loader.get_template('conference.html')
        context = {
            'conference': thisMeeting,
            'isfavorite':isfavorite
        }
        return HttpResponse(template.render(context, request))

    @action(methods=['GET'],detail=False)
    def osearch(self, request):
        queryset = Meeting.objects.all()
        word = request.query_params.get('s', None)
        if word is not None:
            queryset = Meeting.objects.filter(title__contains = word)
        serializer = MeetingSerializer(queryset, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    @action(methods=['GET'],detail=False)
    def allpaper(self, request):
        pk = request.query_params.get('pk', None)
        thismeeting = Meeting.objects.get(meeting_id=pk)
        papers = thismeeting.paper_set.all()
        template = loader.get_template('judgement.html')
        context = {
            'papers': papers,
        }
        return HttpResponse(template.render(context, request))