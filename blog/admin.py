from django.contrib import admin
from .models import Post  #Post가 선언 된 파일을 가져오기

# Register your models here.
admin.site.register(Post)  #Post 모델을 선언해주어야 admin 사이트에 Post 모델이 등록됨