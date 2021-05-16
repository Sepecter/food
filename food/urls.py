"""food URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from community import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'article', views.Article.as_view()),
    path(r'comment', views.Comment.as_view()),
    path(r'userStar', views.UserStar.as_view()),
    path(r'userLike', views.UserLike.as_view()),
    path(r'userInfo', views.UserInfo.as_view()),
    path(r'like', views.Like.as_view()),
    path(r'star', views.Star.as_view()),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)