from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
# from django.core.paginator import Paginator

# Create your views here.


class IndexPage(TemplateView):
    template_name = "blog/index.html"


class BlogListPage(TemplateView):
    def get(self, request):
        blog = Article.objects.all().order_by('-created_time')[:6]
        context ={
            'blog': blog
        }
        
        return render(request,"blog/blog_list.html",context)
        