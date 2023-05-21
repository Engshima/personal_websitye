from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
# from .models import *
from django.db import models

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .serializers import *
import json


# Create your views here.


class IndexPage(TemplateView):
    template_name = "blog/index.html"


class BlogListPage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'blog/blog_list.html'

    def get(self, request):
        gueryset = Article.objects.all().order_by('-created_time')
        paginator = Paginator(gueryset, 3)
        page_number = request.GET.get('page')
        blog_list = paginator.get_page(page_number)
        return Response({'blog_list': blog_list})


class BlogdetailPageView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'blog/blog_details.html'

    def get(self, request, pk): 
       
        blog = get_object_or_404(Article, pk=pk)
        serializer = BlogDetailSerizlizer(blog, many=True)
        categories = Category.objects.all()
        recent = Article.objects.all().order_by("-created_time")
        tag = Tag.objects.all()
        comment = Comment.objects.all()
        return Response({'serializer': serializer, 'blog': blog, 'categories': categories, 'recent': recent, 'tag': tag, 'comment': comment})

    def post(self, request, pk):
        global message
        article = Article.objects.get(pk=pk)
        comment=Comment.objects.filter(pk=pk)
        if comment=="":
           name = request.data["name"] 
           email = request.data["email"]
           message = request.data["message"]
           Comment.objects.create(post=article, name=name,
                               email=email, message=message).save
          
        else:
            parent= Comment.objects.get(pk=pk)
            name = request.data["name"] 
            message = request.data["message"]
            Comment.objects.create(post=article, message=message,name=name ,parent=parent).save
               
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        print(request.data)  # which will print json format of your data
                
        
            
            

class blog_category(TemplateView):
    model: Category
    template_name = 'blog/blog_list.html'


class blog_tag(TemplateView):
    model: Tag
    template_name = 'blog/blog_list.html'


class ContactPage(TemplateView):
    template_name = "blog/contact_us.html"
