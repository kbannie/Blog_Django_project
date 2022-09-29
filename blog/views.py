from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView

# Create your views here.
class PostList(ListView):
    model=Post
    ordering = '-pk'
    # 템플릿 모델명_list.html : post_list.html4
    # 파라미터 모델명_list : post_list

class PostDetail(DetailView):
    model=Post
    # 템플릿 모델명_detail.html : post_detail.html
    # 파라미터 모델명 : post

# def index(request):
#     posts1=Post.objects.all().order_by('-pk');  # -pk : 역순으로
#     return render(request, 'blog/index.html', {'posts':posts1})  #두번째 인자는 template 폴더에서 찾음  #오른쪽 posts가 위에서 선언한 posts

# def single_post_page(request,pk):
#     post2=Post.objects.get(pk=pk)  #get : 특정한 거만 가져오기  #post가 가지고 있는 필드 이름=위에서 받은 인자
#     return render(request,'blog/single_post_page.html',{'post':post2})
