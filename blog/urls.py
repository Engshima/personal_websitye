from django.urls import path
from .import views

app_name = "blog"

urlpatterns = [
    path("",  views.IndexPage.as_view(), name="index"),
    path("bloglist/",views.BlogListPage.as_view(), name="blog"),
    path("blogdetail/<int:pk>/",views.BlogdetailPage.as_view(), name="blog_detail"),
    path("category/<slug:category>/", views.blog_category.as_view(), name="category"),
    path("tag/<slug:tag>/", views.blog_tag.as_view(), name="tag"),
    path("contact/",views.ContactPage.as_view(), name="contact"),

]