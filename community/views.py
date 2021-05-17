from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from community import models
from django.http import JsonResponse
from django.conf import settings
import json


class Article(APIView):

    def get(self, request):
        ret = {'article': []}
        address = request.GET.get('address')
        article_id = request.GET.get('id')
        article_list = []
        if address:
            article_list = models.ArticlePost.objects.filter(address=address)
        elif article_id:
            article_list = models.ArticlePost.objects.filter(id=article_id)
        for i in article_list:
            obj = {
                'id': i.id,
                'poster': i.poster,
                'title': i.title,
                'content': i.content,
                'likes' : i.likes,
                'stars': i.stars,
                'address': i.address,
                'comment': i.comments,
                'time': i.created_time,
            }
            imgs = i.imgtoarticle_set.all()
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

class UserInfo(APIView):

    def get(self, request):
        user_id = request.GET.get('id')
        user = models.User.objects.filter(id=user_id).first()
        ret = {
            'username' : user.username,
            'avatar' : str(user.avatar),
            'usertype' : user.usertype,
        }
        return JsonResponse(ret)

class UserLike(APIView):

    def get(self, request):
        ret = {'comment': []}
        ret = {'article': []}
        user_id = request.GET.get('id')
        comment = models.LikeToComment.objects.filter(user=user_id)
        for i in comment:
            ret['comment'].append(i.comment_id)
        article = models.LikeToArticle.objects.filter(user=user_id)
        for i in article:
            ret['article'].append(i.article_id)
        return JsonResponse(ret)


class UserStar(APIView):

    def get(self, request):
        ret = {'article': []}
        user_id = request.GET.get('id')
        article_star = models.Star.objects.filter(user=user_id)
        for i in article_star:
            ret['article'].append(i.article_id)
        return JsonResponse(ret)

class Comment(APIView):

    def get(self, request):
        ret = {'comment': []}
        article = request.POST.get('article')
        tmp_list = models.Comment.objects.filter(article_id=article)
        for i in tmp_list:
            obj = {
                'poster': i.poster,
                'comment': i.comment,
                'father': i.father,
                'time': i.created_time,
                'likes': i.likes
            }
            imgs = i.imgtocomment_set.all()
            obj['img'] = []
            for img in imgs:
                obj['img'].append(img.img)
            ret['comment'].append(obj)

        ret['code'] = ''
        return JsonResponse(ret)


    def post(self, request):
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

class Star(APIView):

    def get(self, request):
        ret = {}
        article_id = request.GET.get('id')
        user = request.GET.get('user')
        obj = models.Star.objects.filter(article_id=article_id, user=user)
        ret['result'] = '0'
        if obj:
            ret['result'] = 1
        return JsonResponse(ret)

    def post(self, request):
        ret = {}
        user = request.GET.get('user')
        article_id = request.GET.get('id')
        star = models.Star()
        star.article_id = article_id
        star.user = user
        star.save()
        article = star.article
        article.stars = article.stars + 1
        article.save()
        ret['code'] = ''
        return JsonResponse(ret)

    def delete(self, request):
        ret = {}
        user = request.GET.get('user')
        article_id = request.GET.get('id')
        article = models.ArticlePost.objects.get(id=article_id)
        article.likes = article.stars - 1
        article.save()
        models.Star.objects.filter(article_id=article_id, user=user).delete()
        return JsonResponse(ret)

class Like(APIView):

    def get(self, request):
        ret = {}
        like_type = request.GET.get('type')
        object_id = request.GET.get('id')
        user = request.GET.get('user')
        if like_type == 1:
            obj = models.LikeToArticle.objects.filter(article_id=object_id, user=user)
        else :
            obj = models.LikeToComment.objects.filter(comment_id=object_id, user=user)
        ret['result'] = '0'
        if obj:
            ret['result'] = 1
        return JsonResponse(ret)

    def post(self, request):
        ret = {}
        user = request.GET.get('user')
        object_id = request.GET.get('id')
        like_type = request.GET.get('type')
        if like_type == 1:
            like = models.LikeToComment()
            like.comment_id = object_id
            like.user = user
            like.save()
            comment = like.comment
            comment.likes = comment.likes + 1
            comment.save()
        else :
            like = models.LikeToArticle()
            like.article_id = object_id
            like.user = user
            like.save()
            article = like.article
            article.likes = article.likes + 1
            article.save()
        ret['code'] = ''
        return JsonResponse(ret)

    def delete(self, request):
        ret = {}
        user = request.GET.get('user')
        object_id = request.GET.get('id')
        like_type = request.GET.get('type')
        if like_type == 1:
            comment = models.Comment.objects.get(id=object_id)
            comment.likes = comment.likes - 1
            comment.save()
            models.LikeToComment.objects.filter(comment_id=object_id, user=user).delete()
        else :
            article = models.ArticlePost.objects.get(id=object_id)
            article.likes = article.likes - 1
            article.save()
            models.LikeToComment.objects.filter(comment_id=object_id, user=user).delete()
        return JsonResponse(ret)
