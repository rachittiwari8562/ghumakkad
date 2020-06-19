from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from opencage.geocoder import OpenCageGeocode
import requests, json
import datetime
from .models import Comments,District,Place,Blog,Contact,Sd
from .forms import BlogForm
from django.template.loader import render_to_string
from django.http import JsonResponse
import random
import os
from django.core.mail import send_mail
from django.http import FileResponse
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from ghoomketu.settings import GEOCODER_KEY,WEATHER_KEY
geocoder = OpenCageGeocode(GEOCODER_KEY)
base_url = "http://api.openweathermap.org/data/2.5/onecall?"
from ghoomketu.settings import EMAIL_HOST_USER
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.clickjacking import xframe_options_exempt
# Create your views here.
x=0
y=0
def home(request):
    if request.method=="GET":
        if request.is_ajax():
            jagah=request.GET['jagah']
            mapping=render_to_string(template_name=jagah+".html")
            data={"mapping":mapping}
            return JsonResponse(data=data,safe=False)
        else:
            blogs=Blog.objects.filter(published="yes")
            all_blogs=blogs
            if blogs:
                l=len(blogs)
                if l>3:
                    all_blogs=blogs[0:3]
            return render(request,'home.html',{'all_blogs':all_blogs})
    elif request.method=="POST":
        if 'name' in request.POST:
            new_contact=Contact()
            new_contact.by=request.POST['name']
            new_contact.message=request.POST['message']
            new_contact.save()
            subject=request.POST['name']+' contacted you'
            message='name '+request.POST['name']+'\n'+request.POST['message']
            recepient=['rachit8562@gmail.com']
            send_mail(subject, message, EMAIL_HOST_USER, recepient, fail_silently = True)
            return JsonResponse({'done':'yes'},safe=False)
        else:
            data="none"
            global x
            global y
            x=0
            y=0
            if 'latitude' in request.POST:
                x=float(request.POST['latitude'])
                y=float(request.POST['longitude'])
                results = geocoder.reverse_geocode(x,y)
                k=results[0]['components']
                data="none"
                state="none"
                if 'state' in k:
                    statue=k['state']
                    if 'state_district' in k:
                        data=k['state_district']
                        if statue=="Delhi":
                            data="Delhi"
                    elif 'city' in k:
                        data=k['city']
                    elif 'county' in k:
                        data=k['county']
                    else:
                        data="none"
                else:
                    statue="none"
                    data="none"
            elif 'states' in request.POST:
                data=request.POST['states']
                statue=request.POST['jila']
            return redirect(reverse('showplace',args=[statue,data]))
def show_place(request,statue,state):
    if request.method=="GET":
        select=District.objects.filter(state=statue,district=state)
        places=Place.objects.filter(state=statue,district=state)
        if x==0 and y==0:
            if select:
                select1=select[0]
                lat=select1.lat
                longi=select1.longi
            else:
                return render(request,'error.html',{})
        else:
            lat=str(x)
            longi=str(y)
            if len(select)==0:
                complete_url = base_url+"lat="+str(lat)+"&lon="+str(longi)+"&exclude=minutely,hourly&units=metric&appid="+WEATHER_KEY
                response = requests.get(complete_url)
                r = response.json()
                current=r['current']
                c_temp=current['temp']
                c_humid=current['humidity']
                c_wind=current['wind_speed']
                c_des=current['weather'][0]['description'].upper()
                c_icon=current['weather'][0]['icon']
                now = datetime.datetime.now()
                tod=datetime.date.today()
                today=tod.strftime("%B %d, %Y")
                divas=now.strftime("%A")
                a=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
                all=[]
                ind=a.index(now.strftime("%A"))
                din=a[ind:7]+a[0:ind]
                daily=r['daily']
                for i in range(0,6):
                    all.append([daily[i]['weather'][0]['icon'],din[i+1],daily[i]['temp']['day']])
                context={"name":state,"c_temp":c_temp,"c_humid":c_humid,"c_wind":c_wind,"c_des":c_des,"c_icon":c_icon,'today':today,'divas':divas,'all':all}
                return render(request,'state.html',context=context)
        complete_url = base_url+"lat="+str(lat)+"&lon="+str(longi)+"&exclude=minutely,hourly&units=metric&appid="+WEATHER_KEY
        response = requests.get(complete_url)
        r = response.json()
        current=r['current']
        c_temp=current['temp']
        c_humid=current['humidity']
        c_wind=current['wind_speed']
        c_des=current['weather'][0]['description'].upper()
        c_icon=current['weather'][0]['icon']
        now = datetime.datetime.now()
        tod=datetime.date.today()
        today=tod.strftime("%B %d, %Y")
        divas=now.strftime("%A")
        a=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
        all=[]
        ind=a.index(now.strftime("%A"))
        din=a[ind:7]+a[0:ind]
        daily=r['daily']
        for i in range(0,6):
            all.append([daily[i]['weather'][0]['icon'],din[i+1],daily[i]['temp']['day']])
        all_comments=Comments.objects.filter(state=statue,name_district=state)
        length=len(all_comments)
        another=[]
        if length>12:
            b=length//12
            another=['1','2','3','4','5','6','7','8','9','10','11','12']*b
            length=length%12
        sample=another+random.sample(['1','2','3','4','5','6','7','8','9','10','11','12'],length)
        all_comments=zip(sample,all_comments)
        all_places=[]
        all_places=Place.objects.filter(state=statue,district=state)
        select1=select[0]
        blogs=Blog.objects.filter(state=statue,district=state)
        context={"name":state,"c_temp":c_temp,"c_humid":c_humid,"c_wind":c_wind,"c_des":c_des,"c_icon":c_icon,'today':today,'divas':divas,'all':all,'all_comments':all_comments,'all_places':all_places,"state":select1,"blogs":blogs,"places":places}
        return render(request,'state.html',context=context)
    else:
        name=request.POST['name']
        message=request.POST['message']
        if name=='' or message=='':
            return JsonResponse(data={'error':"yes"},safe=False)
        else:
            new_comment=Comments()
            new_comment.state=statue
            new_comment.name_district=state
            new_comment.by=name
            new_comment.content=message
            new_comment.save()
            sample=random.choice(['1','2','3','4','5','6','7','8','9','10','11','12'])
            saare_comments=render_to_string(template_name="comment.html",context={'comment':new_comment,'sample':sample})
            data={"saare_comments":saare_comments,"error":'no'}
            return JsonResponse(data=data,safe=False)
def show_blog(request):
    if request.is_ajax():
        if request.method=="GET":
            other=District.objects.filter(state=request.GET['stut'])
            sorry=render_to_string(template_name="options.html",context={'district':other})
            return JsonResponse({'sorry':sorry},safe=False)
        else:
            form=BlogForm(request.POST,request.FILES)
            if form.is_valid():
                blog=Blog()
                blog.by=form.cleaned_data['by']
                blog.state=form.cleaned_data['state']
                blog.district=form.cleaned_data['district']
                blog.published=form.cleaned_data['published']
                blog.file=form.cleaned_data['file']
                blog.photo=form.cleaned_data['photo']
                blog.description=form.cleaned_data['description']
                blog.save()
                return JsonResponse({'error':'no','upload':'done'},safe=False)
            else:
                return JsonResponse(form.errors,safe=False)
    else:
        blogs_list=Blog.objects.filter(published="yes")
        page=request.GET.get('page',1)
        paginator = Paginator(blogs_list,12)
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)
        district=District.objects.filter(state='Andhra Pradesh')
        return render(request,'blog.html',{'all_blogs':blogs,'district':district})
