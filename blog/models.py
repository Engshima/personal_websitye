from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from ckeditor.fields import RichTextField
from datetime import datetime
from django.urls import reverse

def  validate_file_extentions(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    valid_extentions = ['.jpg', '.png','.jpeg']
    if not ext.lower() in valid_extentions:
        raise ValidationError('Unsupported File Extention.')
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.FileField(
        upload_to='files/user_avatar/', blank=False, null=False, validators=[validate_file_extentions])
    description = models.CharField(max_length=512, null=False, blank=False)
    class Meta:
          managed = True
          verbose_name = 'پروفایل کاربران'
          verbose_name_plural  = 'پروفایل کاربران'
    
    def __str__(self):
        return self.user.first_name + "" + self.user.last_name
    
    def __str__(self):
        return f"{self.user}"

class Article(models.Model):
    title = models.CharField(max_length=128, blank=False, null=False)
    cover = models.FileField(
        upload_to='files/article_cover/', null=False, blank=False, validators=[validate_file_extentions])
    content = RichTextField()
    created_time = models.DateTimeField(
        default=datetime.now, blank=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="category")
    tag = models.ManyToManyField("Tag", verbose_name=_("تگ ها"), related_name="tags", blank=True)
    author = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    comment = models.ManyToManyField("Comment", verbose_name=_("کامنت ها"), related_name="comments", null=True,blank=True)
    class Meta:
          managed = True
          verbose_name = 'مقاله ها'
          verbose_name_plural  = 'مقاله ها'
    
    def  __str__(self):
        return self.title
        
   
    
class Category(models.Model):
    title = models.CharField(max_length=128, null=False, blank=False)
    cover = models.FileField(upload_to='files/article_cover/', null=False, blank=False, validators=[validate_file_extentions])
    slug = models.SlugField(_("عنوان لاتین"), null=True)
    
    class Meta:
          managed = True
          verbose_name = 'دسته بندی'
          verbose_name_plural  ='دسته بندی ها'
    
    def __str__(self):
        return self.title
    def get_absolute_url(self):
            return reverse("blog_detail", kwargs={"slug": self.slug})

class Tag(models.Model):
     title = models.CharField(_("عنوان"), max_length=254) 
     slug = models.SlugField(_("عنوان لاتین"),null=True)
     published_at  = models.DateTimeField(_("تاریخ انتشار"),auto_now=False, auto_now_add=True)      
     updated_at  = models.DateTimeField(_("تاریخ بروزرسانی"),auto_now=True, auto_now_add=False)
     
     class Meta:
          managed = True
          verbose_name = 'تگها'
          verbose_name_plural  = 'تگها'
    
     def __str__(self):
        return self.title
     def get_absolute_url(self):
            return reverse("blog_detail", kwargs={"slug": self.slug}) 
class Comment(models.Model):
    
      post = models.ForeignKey("Article", verbose_name=_("مقاله"), related_name="comments",on_delete=models.CASCADE) 
      name = models.CharField(_("نام کاربر"), max_length=254)
      email = models.EmailField(_("آدرس الکترونیکی"), max_length=254)
      message = models.TextField(_("متن نظر"))
      image  = models.ImageField(null=True, blank=True,upload_to='files/article_cover/', height_field=None, width_field=None, max_length=100, default=False)
      date =  models.DateField(_("تاریخ انتشار"), auto_now=False, auto_now_add=True)
      active = models.BooleanField(_("فعال"),default=True)
      parent= models.ForeignKey('self', verbose_name=_("پاسخ ها"),related_name="replies", on_delete=models.CASCADE, null=True, blank=True)
      
      class Meta:
          managed = True
          verbose_name = 'نظرات'
          verbose_name_plural  = 'نظرات'
          
      def  __str__(self):
           return self.email
      
      def __str__(self):
            return f"{self.name}" 
        
      @property
      def children(self):
        return Comment.objects.filter(parent=self).reverse()
      
      @property
      def is_parent(self):
        if self.parent is None:
            return True
        return False           