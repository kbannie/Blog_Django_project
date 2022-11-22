from django.contrib import admin
from .models import Post,Category, Tag, Comment  #Post가 선언 된 파일을 가져오기

# Register your models here.
admin.site.register(Post)  #Post 모델을 선언해주어야 admin 사이트에 Post 모델이 등록됨

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name', )}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name', )}

admin.site.register(Category, CategoryAdmin)

admin.site.register(Tag, TagAdmin)

admin.site.register(Comment)