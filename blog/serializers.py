from rest_framework import serializers
from .models import *


class BlogDetailSerizlizer(serializers.ModelSerializer):
    class Meta:
       model = Article
       fields = ['title','cover','content','created_time','category','author']

    
    
    

       
