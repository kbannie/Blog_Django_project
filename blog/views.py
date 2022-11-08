from django.shortcuts import render, redirect
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

#CBV 사용했을 때
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model=Post
    fields=['title','hook_text', 'content','head_image','file_upload','category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


    def form_valid(self, form):
        current_user=self.request.user
        if current_user.is_authenticated and (current_user.is_superusr or current_user.is_staff):
            form.instance.author=current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')


    #템플릿 : 모델명_form.html
    def get_context_data(self, *, object_list=None, **kwargs):
        context=super(PostCreate, self).get_context_data()
        context['categories']=Category.objects.all()
        context['no_category_post_count']=Post.objects.filter(category=None).count
        return context

class PostList(ListView):
    model=Post
    ordering = '-pk'
    # 템플릿 모델명_list.html : post_list.html4
    # 파라미터 모델명_list : post_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super(PostList, self).get_context_data()
        context['categories']=Category.objects.all()
        context['no_category_post_count']=Post.objects.filter(category=None).count
        return context

class PostDetail(DetailView):
    model=Post
    # 템플릿 모델명_detail.html : post_detail.html
    # 파라미터 모델명 : post

    def get_context_data(self, **kwargs):
        context=super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context

def category_page(request, slug):
    if slug=='no_category' :
        category ='미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category=Category.objects.get(slug=slug)
        post_list=Post.objects.filter(category=category)
    return render(request, 'blog/post_list.html',{
        'category':category,
        'post_list':post_list,
        'categories':Category.objects.all(),
        'no_category_post_count':Post.objects.filter(category=None).count
    })

def tag_page(request, slug):
    tag=Tag.objects.get(slug=slug)
    post_list=tag.post_set
    return render(request, 'blog/post_list.html', {
        'tag':tag,
        'post_list':post_list,
        'categories': Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count
    })

#FBV 사용했을 때
# def index(request):
#     posts1=Post.objects.all().order_by('-pk');  # -pk : 역순으로 #Post 모델에 있는 모든 것들을 posts1에 넣음 -> 템플릿에서 사용된 데이터를 views에서 준비
#     return render(request, 'blog/index.html', {'posts':posts1})  #두번째 인자는 template 폴더에서 찾음  #오른쪽 posts1가 위에서 선언한 posts1

# def single_post_page(request,pk):  #pk에 따라 불러오는 글이 달라지니 views 쪽에 pk도 전달해야 함
#     post2=Post.objects.get(pk=pk)  #get : 특정한 거만 가져오기  #Post가 가지고 있는 필드 이름=위에서 받은 인자
#     return render(request,'blog/single_post_page.html',{'post':post2})