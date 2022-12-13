from django.contrib import admin
from .models import *

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','avatar','description']

admin.site.register(UserProfile,UserProfileAdmin)    

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title','cover','author']
    
admin.site.register(Article,ArticleAdmin)    

class CategoryAdmin(admin.ModelAdmin):
  list_display = ['title','cover']
    
admin.site.register(Category,CategoryAdmin)      