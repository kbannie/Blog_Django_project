from django.db import models
from django.contrib.auth.models import User
import os

# Model이 변경될 때 마다 꼭 해주기!!!
# python manage.py makemigrations
# python manage.py migrate

class Tag(models.Model):
    name=models.CharField(max_length=50, unique=True)
    slug=models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'


class Category(models.Model):
    name=models.CharField(max_length=50, unique=True)
    slug=models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}'
    class Meta:
        verbose_name_plural='Categories'

class Post(models.Model): #Post 모델 생성
    title=models.CharField(max_length=30) #Post 모델의 필드 생성  #CharField():길이 제한을 해줄 때
    hook_text=models.CharField(max_length=100,blank=True) #사용자가 미리보기 제공 안해도 ok
    content=models.TextField()            #TextField():길이 제한 없을 때

    head_image=models.ImageField(upload_to='blog/images/%Y/%m/%d/',blank=True)
    #%Y 2022(4자리) / %y 22(2자리)
    file_upload=models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    #한국 시간에 맞추기 위해서는 '프로젝트 - settings.py'에서 TIME_ZONE = 'Asia/Seoul', USE_TZ = False 로 작성해주기
    created_at=models.DateTimeField(auto_now_add=True)  #DateTimeField:날짜, 시간   auto_now_add=True:자동으로 시간 부여
    updated_at=models.DateTimeField(auto_now=True)

    #추후 author 작성
    author=models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    category=models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags=models.ManyToManyField(Tag, blank=True)

    def __str__(self):  #Model안의 내용을 화면에 출력하는 기능
        return f'[{self.pk}]{self.title}::{self.author}:{self.created_at}'  #게시글을 만들 때 마다 고유의 키를 부여함 -> pk(primary key)

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'   #문자열 만들기

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)  #파일명만 가져오기

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]  #split('.') : .으로 구분하기
        # 배열이니 a가 [0]번지, txt가 [1]번지
        # a.txt  -> a txt
        # b.docx -> b docx
        # c.xlsx -> c xlsx
        # 하지만 a.b.c.txt -> a b c txt  1번지로 하면 b이니 마지막에 있는 것으로 지정하기 [-1]

