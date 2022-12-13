from django.urls import path
from .import views

app_name = "blog"

urlpatterns = [
    path("",  views.IndexPage.as_view(), name="index"),
    path("bloglist/",views.BlogListPage.as_view(), name="bloglist")
]