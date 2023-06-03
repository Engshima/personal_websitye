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
        search= Article.objects.filter(title__icontains = 'برنامه').values()  
        serializer = BlogDetailSerizlizer(blog, many=True)
        categories = Category.objects.all()
        recent = Article.objects.all().order_by("-created_time")
        tag = Tag.objects.all()
        comment = Comment.objects.all()
        return Response({'serializer': serializer, 'blog': blog, 'categories': categories, 'recent': recent, 'tag': tag, 'comment': comment, 'search': search})

    def post(self, request, pk):
        global message
        article = Article.objects.get(pk=pk)
        parent_comment_id = request.POST.get('parent_id')
        parent_comment = None
        if parent_comment_id:
           try:
               parent_comment = Comment.objects.get(id=parent_comment_id)
           except Comment.DoesNotExist:
               pass
           
        if not parent_comment :
            email = request.data["email"]
            message = request.data["message"]
            name = request.data["name"]
            Comment.objects.create(post=article, name=name,
                               email=email, message=message).save       
           
        else:
               
            message = request.data["message"]
            email = request.data["email"]
            name = request.data["name"]
            Comment.objects.create(post=article, name=name,
                               message=message,email=email,parent=parent_comment).save 
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
     
       
                
        
            
            

class blog_category(TemplateView):
    model: Category
    template_name = 'blog/blog_list.html'


class blog_tag(TemplateView):
    model: Tag
    template_name = 'blog/blog_list.html'




class ContactPage(TemplateView):
    template_name = "blog/contact_us.html"

