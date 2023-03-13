from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from .models import *

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


# Create your views here.


class IndexPage(TemplateView):
    template_name = "blog/index.html"
    
class BlogListPage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'blog/blog_list.html'
    def get(self,request):
        gueryset = Article.objects.all().order_by('-created_time')  
        paginator = Paginator(gueryset,3)
        page_number = request.GET.get('page')
        blog_list = paginator.get_page(page_number) 
        return Response({'blog_list': blog_list})
    
class BlogdetailPage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'blog/blog_details.html'
    
    def  get(self, request,pk):
        blog = get_object_or_404(Article,pk=pk)
        serializer = BlogDetailSerizlizer(blog)
        categories = Category.objects.all()
        recent = Article.objects.all().order_by("-created_time")
        tag = Tag.objects.all()
        comment = Comment.objects.all()
        return Response({'serializer':serializer,'blog':blog, 'categories':categories, 'recent':recent, 'tag':tag, 'comment':comment})
    
    def  post(self,request,pk):
        from django.shortcuts import redirect
        comment = get_object_or_404(Comment,pk=pk)
        serializer=  CommentSerializer(comment,data=request.data)
        if not serializer.is_valid():
            return Response({'serializer':serializer,'comment':comment})
        serializer.save()
        return redirect('http://127.0.0.1/blogdetail/1/')
        
    
    
    def put(self, request,pk):
        from django.shortcuts import redirect
        new_comment = get_object_or_404(Comment, pk=pk)
        serializer=  CommentSerializer(instance=new_comment,data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
                
class blog_category(TemplateView):
       model:Category
       template_name = 'blog/blog_list.html'
       
class blog_tag(TemplateView):
    model: Tag
    template_name = 'blog/blog_list.html'

class ContactPage(TemplateView):
    template_name ="blog/contact_us.html"
    
    

 
    
        