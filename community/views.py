from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from community import models
from django.http import JsonResponse
from django.conf import settings
import json


class Article(APIView):

    def get(self, request):
        ret = {}
        ret['article'] = []
        address = request.GET.get('address')
        list = models.ArticlePost.objects.filter(address=address)
        for var in list:
            obj = {
                'id': var.id,
                'poster': var.poster,
                'title': var.title,
                'content': var.content,
                'address': var.address,
                'likes': var.likes,
                'comment': var.comment,
                'time': var.time,
            }
            imgs = var.img_set.all()
            ret['img'] = []
            for img in imgs:
                ret['img'].append(img.img)
            ret['article'].append(obj)
        ret['code'] = ''
        return JsonResponse(ret)

    def post(self, request):
        ret = {}
        poster = request.POST.get('poster')
        print(poster)
        title = request.POST.get('title')
        content = request.POST.get('content')
        images = request.FILES.getlist('images')
        address = request.POST.get('address')
        article = models.ArticlePost.objects.create(poster=poster, title=title, content=content, address=address)
        for img in images:
            p = models.Img()
            p.img = img
            p.article_id = article.id
            p.save()
            pname = '%s/img/%s' % (settings.MEDIA_ROOT, img.name)
            print(p.img)
            with open(pname, 'wb') as f:
                for content in img.chunks():
                    f.write(content)
        ret['code'] = ''
        return JsonResponse(ret)
