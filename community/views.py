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
                'comment': var.comments,
                'time': var.created_time,
            }
            imgs = var.imgtoarticle_set.all()
            obj['img'] = []
            for img in imgs:
                obj['img'].append(str(img.img))
            ret['article'].append(obj)
        ret['code'] = ''
        return JsonResponse(ret)

    def post(self, request):
        ret = {}
        poster = request.POST.get('poster')
        title = request.POST.get('title')
        content = request.POST.get('content')
        images = request.FILES.getlist('images')
        address = request.POST.get('address')
        article = models.ArticlePost.objects.create(poster=poster, title=title, content=content, address=address)
        for img in images:
            p = models.ImgToArticle()
            p.img = img
            p.article_id = article.id
            p.save()
            pname = '%s/img/%s' % (settings.MEDIA_ROOT, img.name)
            with open(pname, 'wb') as f:
                for content in img.chunks():
                    f.write(content)
        ret['code'] = ''
        return JsonResponse(ret)

class Comment(APIView):

    def get(self,request):
        ret = {}
        ret['comment'] = []
        artilce = request.POST.get('article')
        list = models.Comment.objects.filter(article_id=artilce)
        for var in list:
            obj = {
                'poster': var.poster,
                'comment': var.comment,
                'father': var.father,
                'time': var.created_time,
                'likes': var.likes
            }
            imgs = var.imgtocomment_set.all()
            obj['img'] = []
            for img in imgs:
                obj['img'].append(img.img)
            ret['comment'].append(obj)

        ret['code'] = ''
        return JsonResponse(ret)

    def post(self,request):
        ret = {}
        article = request.POST.get('article')
        poster = request.POST.get('poster')
        comment = request.POST.get('comment')
        father = request.POST.get('father')
        images = request.FILES.getlist('images')
        comment = models.Comment.objects.create(
            article_id=article,
            poster=poster,
            comment=comment,
            father=father,
        )
        art = models.ArticlePost.objects.get(id=article)
        art.comments = art.comments + 1
        art.save()
        for img in images:
            p = models.ImgToComment()
            p.img = img
            p.article_id = article.id
            p.save()
            pname = '%s/img/%s' % (settings.MEDIA_ROOT, img.name)
            with open(pname, 'wb') as f:
                for content in img.chunks():
                    f.write(content)
        ret['code'] = ''
        return JsonResponse(ret)

class Like(APIView):

    def get(self,request):
        ret = {}
        id = request.GET.get('id')
        user = request.GET.get('user')
        obj = models.Like.objects.filter(comment_id=id,user=user)
        ret['reuslt'] = '0'
        if obj:
            ret['reuslt'] = 1
        return JsonResponse(ret)

    def post(self,request):
        ret = {}
        user = request.POST.get('uesr')
        id = request.GET.get('id')
        like = models.Like()
        like.comment_id = id
        like.user = user
        like.save()
        comment = like.comment
        comment.likes = comment.likes+1
        comment.save()
        ret['code'] = ''
        return JsonResponse(ret)

    def delete(self,request):
        ret = {}
        user = request.POST.get('uesr')
        id = request.GET.get('id')
        comment = models.Comment.objects.get(id=id)
        comment.likes = comment.likes - 1
        comment.save()
        models.Like.objects.filter(comment_id=id,user=user).delete()
        return JsonResponse(ret)