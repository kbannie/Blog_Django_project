## 5. bootstrap 연결하기
###(1) blog/static/blog 폴더 만들고 bootstrap 관련 css 넣어주기
###(2) blog/templates/blog/post_list.html 수정 및 추가
- 미리 만들어 둔 bootstrap을 적용한 blog_list.html 코드를 다 넣어버리기
- post_list.html 상단에 코드 추가 및 수정
```python
{% load static %}
<head>
    ...
    <link href="{% static 'blog/bootstrap/css/bootstrap.min.css' %}" rel="stylesheet" type="text/css" media="screen"></link>
    #경로에 맞게 작성해주면 됨
    #media="screen" : 이거도 추가해주기
    ...
</head>
```
- Featured blog  post 부분 수정
```python
{% for p in post_list %}
<div class="card mb-4">
    <a href="#!"><img class="card-img-top" src="https://picsum.photos/seed/{{p.pk}}/800/200" alt="random image"/></a>
    <div class="card-body">
        <h2 class="card-title">{{p.title}}</h2>
        <p class="card-text">{{p.content}}</p>
        <a class="btn btn-primary" href="{{p.get_absolute_url}}">Read more →</a>
    </div>
    <div class="card-footer">
        <div class="small text-muted">{{p.created_at}}</div>
        <a href="#">작성자(추후 개발 예정)</a>
    </div>
</div>
{% endfor %}
```
###(3) blog/templates/blog/post_detail.html 수정 및 추가
#### bootstrap 적용하기
- startbootstrap.com에서 templates  -> Blog Post에서 Free Dowload로 다운받기
- index.html 파일 코드를 post_detail.html에 붙여넣기
- css폴더도 static 폴더 밑에 붙여넣기
- post_detail.html 상단에 코드 추가 및 수정
```python
{% load static %}
<head>
    ...
    <link href="{% static 'blog/bootstrap/css/bootstrap.min.css' %}" rel="stylesheet" type="text/css" media="screen"></link>
    <link href="{% static 'blog/css/styles.css' %}" rel="stylesheet" />
    #경로에 맞게 작성해주면 됨
    #media="screen" : 이거도 추가해주기
    ...
</head>
```
- 하단에 코드 추가
```python
<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.min.js" integrity="sha384-w1Q4orYjBQndcko6MimVbzY0tgp4pWB4lZ7lr30WKz0vr/aWKhXdBNmNb5D92v7s" crossorigin="anonymous"></script>
```
- Page content 부분 수정
```python
<article>
                        <!-- Post header-->
                        <header class="mb-4">
                            <!-- Post title-->
                            <h1 class="fw-bolder mb-1">{{post.title}}</h1>
                            <!-- Post meta content-->
                            <div class="text-muted fst-italic mb-2">Posted on {{post.created_at}} by 작성자(추후 개발 예정)</div>
                            <!-- Post categories-->
                            <a class="badge bg-secondary text-decoration-none link-light" href="#!">Web Design</a>
                            <a class="badge bg-secondary text-decoration-none link-light" href="#!">Freebies</a>
                        </header>
                        <!-- Preview image figure-->
                        <figure class="mb-4">
                            <img class="img-fluid rounded" src="https://picsum.photos/seed/{{post.pk}}/800/200" alt="random image"/>
                            #여기는 다른 문장임
                        </figure>
                        <!-- Post content-->
                        <section class="mb-5">
                            <p class="fs-5 mb-4">{{post.content}}</p>
                        </section>
</article>
```
---
## 6. static 관리하기
###(1) 초기 설정
- main/settings.py
```python
import os #상단에 추가

MEDIA_URL='/media/' #url 경로
MEDIA_ROOT=os.path.join(BASE_DIR,'_media')  #저장되는 폴더의 이름
```
- blog/models.py
```python
import os #파일 경로 갖져오기 위해서 import 해주기

class Post(models.Model):
    ...
    head_image=models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True) #_media/blog/images로 _media는 생략됨
    #blank=True : 이미지 올리는 것이 필수x
    #Y(2022)/ y(22) 년도 표시 차이
    file_upload=models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)
    
    def get_file_name(self):  #파일명 가져오기
        return os.path.basename(self.file_upload.name)
    
    def get_file_ext(self):  #확장자 가져오기
        return self.get_file_name().split('.')[-1] #a.txt b.docx c.xlsx
        #split('.')[-1] .으로 분리하고 배열의 제일 마지막 요소를 -1로 표현
        #a.txt-> a txt
        #b.docx -> b docx
        #c.xlsx -> c xlsx
```
- main/urls.py
```python
from django.conf import settings
from django.conf.urls.static import static

#이미지를 보여주는 패턴을 선언해주기
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
# MEDIA_URL이 들어오면 MEDIA_ROOT와 연결해주기
```
- 미디어 관리를 위해서 cmder에서 가상환경인거 확인 후 
```
pip install Pillow 
```
- models를 변경해주었으니 cmder에서 migrate 하기
```python
python manage.py makemigrations
python manage.py migrate
```

###(2) 이미지 업로드
- admin 페이지에서 이미지 업로드하기
- 업로드 된 이미지를 웹페이지에 보여주기
  - blog/templates/blog/post_list.html
  ```python
  <div class="card mb-4"> #위치 확인용
    {% if p.head_image %}  #이미지를 업로드 했을 때
    <img class="card-img-top" src="{{p.head_image.url}}" alt="{{p.title}}의 head_image" />
     #p.head_image.url 과 연결하기     
    {% else %}  #이미지를 업로드하지 않았을 때
    <img class="card-img-top" src="https://picsum.photos/seed/{{p.pk}}/800/200" alt="random image"/>
    #/seed/{{p.pk}} : pk값에 따라 고유한 이미지 부여 
    #/800/200 : 가로/세로 지정    
    {% endif %}
  ```
  - blog/templates/blog/post_detail.html
  ```python
  <figure class="mb-4">
    {% if post.head_image %}
    <img class="img-fluid rounded" src="{{post.head_image.url}}" alt="{{post.title}}"의 head_image />
    {% else %}
    <img class="img-fluid rounded" src="https://picsum.photos/seed/{{post.pk}}/800/200" alt="random image"/>
    {% endif %}
  </figure>             
  ```

###(3) 첨부파일 업로드
- admin 페이지에서 파일 업로드하기
- 업로드 된 파일을 웹페이지에 보여주기
  - blog/templates/blog/post_detail.html
  ```python
  #fontawsome을 사용하니 head에 아래 코드 넣어주기
  <script src="https://kit.fontawesome.com/87c08dff42.js" crossorigin="anonymous"></script>
  
  {% if post.file_upload %}
    <a href="{{post.file_upload.url}}" class="btn btn-outline-dark" role="button" download>  #download : download 역할을 한다
      {% if post.get_file_ext == 'xlsx' or post.get_file_ext == 'xls' %} #확장자에 따라 다른 아이콘을 삽입하기
      <i class="fa-regular fa-file-excel"></i> #엑셀 아이콘
      {% elif post.get_file_ext == 'docx' or post.get_file_ext == 'doc' %}
      <i class="fa-regular fa-file-word"></i>  #워드 아이콘
      {% else %}
      <i class="fa-regular fa-file"></i>  #파일 아이콘
      {% endif %}
      Download {{post.get_file_name}}
    </a>
  {% endif %}
  ```
---
## 7. 미리보기
###(1) 요약문
- blog/models.py
```python
class Post(models.Model):
    hook_text=models.CharField(max_length=100, blank=True)
```
- models를 변경해주었으니 cmder에서 migrate 하기
```python
python manage.py makemigrations
python manage.py migrate
```
- blog/templates/blog/post_list.html
```python
#title과 content 사이에 입력
{% if p.hook_text %}
<h5 class="text-muted">{{p.hook_text}}</h5>
#class="text-muted" : 회색으로 출력
{% endif %}
```
- blog/templates/blog/post_detail.html
```python
#title 밑에 입력
{% if post.hook_text %}
<h5 class="text-muted">{{post.hook_text}}</h5>
{% endif %}
```
### (2) content 내용 list에서 일부만 보이기
- blog/templates/blog/post_list.html
```python
<p class="card-text">{{p.content | truncatechars:100}}</p>
#truncatechars:100 100자만 출력하기
```
---
##8. 필터 적용
###(1) 대문자, 소문자
- blog/templates/blog/post_list.html
```python
<h2 class="card-title">{{p.title | upper}}</h2>
#upper : 대문자로 출력하기
#lower : 소문자로 출력하기
```
###(2) 시간 표시 변경
- blog/templates/blog/post_list.html
```python
<div class="small text-muted">{{p.created_at | date:"Y-m-d h:m:s"}}</div>
```