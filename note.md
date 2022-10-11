## 1. django 프로젝트 시작
#### (1) 데이터 베이스 생성
```
python manage.py migrate
```
ls 해주면 db.sqlit3 파일이 생성된 것을 보임

#### (2) 관리자 계정 생성
```
python manage.py createsuperuser
```
username, email, password 입력
```
python manage.py runserver
```
admin 페이지에 들어가서 로그인 하면 완료

#### (3) 앱 만들기
```
python manage.py startapp 앱명
```

####(4) Django 프로젝트에 등록하기
main 프로젝트 - settings.py - INSTALLED_APPS 에 만들었던 앱을 추가해 주기
ex) 'blog'

## 2. Model 만들기
**(1) app / models.py 모델 생성**
```py
class Post(models.Model):
    title=models.CharField(max_length=30)
```
####(2) app / admin.py 모델 등록
```py
from .models import Post  #Post가 선언 된 파일을 가져오기
admin.site.register(Post)  #Post 모델을 선언해주어야 admin 사이트에 Post 모델이 등록됨
```
#### (3) migrate 해주기 
```commandline
python manage.py makemigrations
python manage.py migrate
```
#### (4) 시간 설정하기
app/models.py
```py
class Post(models.Model):
    created_at=models.DateTimeField(auto_now_add=True) #시간 자동 부여
    
    def __str__(self):  #Model안의 내용을 화면에 출력하는 기능
        return f'[{self.pk}]{self.title}:{self.created_at}'  
        #게시글을 만들 때 마다 고유의 키를 부여함 -> pk(primary key)
```
main/settings.py
```py
TIME_ZONE = 'Asia/Seoul'
USE_TZ = False
```

## 3. 웹페이지 만들기
### (1) FBV
#### a. 블로그 리스트 페이지

main/urls.py
```python
from django.urls import path, include 
urlpatterns=[
    path('blog/', include('blog.urls'))
]
```
blog/urls.py 만들기
```python
from django.urls import path
from . import views
urlpatterns=[
    path('', views.index)  #views.함수이름
]
```

blog/views.py
```python
from .models import Post

def index(request):
    posts1=Post.objects.all().order_by('-pk') # .order_by('-pk') : 역순으로 
    #Post 모델에 있는 모든 것들을 posts1에 넣음 -> 템플릿에서 사용된 데이터를 views에서 준비
    return render(request, 'blog/index.html', {'posts':posts1})
    #posts 인자는 template 폴더에서 찾음  #오른쪽 posts1가 위에서 선언한 posts1
```

blog/templates/blog/index.html 만들기
```html
{% for p in posts %}
    <h2>{{p.title}}</h2>
    <h3>{{p.created_at}}</h3>
    <p>{{p.content}}</p>
{% endfor %}
```

---
#### b.블로그 상세 페이지
blog/urls.py 만들기
```python
path('<int:pk>/', views.single_post_page)
```

blog/views.py
```python
def single_post_page(request,pk):  #pk에 따라 불러오는 글이 달라지니 views 쪽에 pk도 전달해야 함
     post2=Post.objects.get(pk=pk)  #get : 특정한 거만 가져오기  #Post가 가지고 있는 필드 이름=위에서 받은 인자
     return render(request,'blog/single_post_page.html',{'post':post2})
```

blog/templates/blog/single_post_page.html 만들기
```python
<h1>{{post.title}}</h1>
<h3>{{post.created_at}}</h3>
<p>{{post.content}}</p>
```