#다대일 관계
##1. 작성자 작성
- models.py
```python
from django.contrib.auth.models import User
class Post(models.Model):
    ...
    author=models.ForeignKey(User, null=True, on_delete=models.SET_NULL) #FroreignKey():다대일 관계 
                                                             #on_delete=models.CASCADE:작성자를 삭제할 때 해당 포스트도 삭제
                                                             #on_delete=models.SET_NULL : 작성자를 삭제해도 포스트는 삭제가 되는 것이 아닌 None으로 됨
                                                             #위의 코드를 작성할 때는 null=True도 써줘야 함

    def __str__(self):
        return f'[{self.pk}]{self.title}::{self.author}:{self.created_at}'
```
- cmder
```
python manage.py makemigrations
1
1
python manage.py migrate
```
- admin 페이지에서 user 추가해서 확인하기
- tests.py
```python
from django.contrib.auth.models import User
class TestView(TestCase):
    def setUp(self):
        ...
        self.user_kim=User.objects.create_user(username="kim",password="1111") #user 추가하기
        self.user_lee=User.objects.create_user(username="lee",password="1111")     

    def test_post_list(self):
        ...
        #author 추가하기
        post_001=Post.objects.create(title="첫번째 포스트",content="첫번째 포스트입니다.", author=self.user_kim) 
        post_002=Post.objects.create(title="두번째 포스트",content="두번째 포스트입니다.", author=self.user_lee)
        ...
        #usernmae이 있는지 확인하기
        self.assertIn(post_001.author.username.upper(), main_area.text)  #.upper() : 대문자로 표시하기
        self.assertIn(post_002.author.username.upper(), main_area.text)
        ...

    def test_post_detail(self):
        #author 추가하기
        post_001=Post.objects.create(title="첫번째 포스트",content="첫번째 포스트입니다.", author=self.user_kim) 
        ...
        #usernmae이 있는지 확인하기
        self.assertIn(post_001.author.username.upper(), post_area.text)  #.upper() : 대문자로 표시하기
```
- post_list.html
```python
<a href="#">{{p.author | upper}}</a>
```
- post_detail.html
```python
Posted on {{post.created_at | date:"Y-m-d h:m:s"}} by {{post.author|upper}}
```
##2. 카테고리 작성
###(1) post_list
- models.py
```python
class Category(models.Model):
    name=models.CharField(max_length=50, unique=True)
    slug=models.SlugField(max_length=200, unique=True, allow_unicode=True) #SlugField : 숫자 pk대신 텍스트로 URL 만들기

    def __str__(self):
        return self.name #카테고리 자체의 name을 전달
    
    class Meta:
        verbose_name_plural='Categories'

class Post(models.Model):
    ...
    category=models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL) # blank=True : 카테고리 지정안해도 괜찮
    ...
```
- cmder
migrate 해주기
- admin.py

```python
from .models import Post, Category
...
#name을 작성하면 자동으로 slug도 작성됨
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name', )} #미리 특정한 필드를 지정하기
    
#admin 페이지에서 Category 필드가 나타내게 하기   
admin.site.register(Category, CategoryAdmin) #CategoryAdmin도 추가해주기
```

- tests.py
```python
from  .models import Post, Category

class TestView(TestCase):
    def setUp(self):
        ...
        self.category_com=Category.objects.create(name="computer", slug="computer")
        self.category_cul=Category.objects.create(name="culture", slug="culture")
        
        #def test_post_list에서 만든 post_001과 post_002를 def setUp에서 만들어주기
        #category 필드도 추가해 주어서 category 테스트하기 
        self.post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다.", author=self.user_kim, category=self.category_com)
        self.post_002 = Post.objects.create(title="두번째 포스트",content="두번째 포스트입니다.", author=self.user_lee, category=self.category_cul)
        self.post_003 = Post.objects.create(title="세번째 포스트",content="세번째 포스트입니다.", author=self.user_lee)

    def nav_test(self, soup):
        ...
        home_btn=navbar.find('a', text="Home") #a태그에 Home이 있는거 찾기  #Home 뒤에 다른 태그가 있거나 하면 오류가 발생함
        self.assertEqual(home_btn.attrs['href'], "/")  #그 태그의 속성이 /인가
        blog_btn=navbar.find('a', text="Blog") 
        self.assertEqual(blog_btn.attrs['href'], "/blog/")
        about_btn=navbar.find('a', text="AboutMe") 
        self.assertEqual(about_btn.attrs['href'], "about_me.html")
    
    #4.
    def category_test(self, soup):
        category_card=soup.find('div', id='category-card') #test 영역 줄이기
        self.assertIn('Categories', category_card.text) #Categories가 category_card에 있는지
        #6.
        self.assertIn(f'{self.category_com} ({self.category_com.post_set.count()})', category_card.text) #category_com이 category_card에 있는지
        #필드명 말고 count도 출력하니 f''로 묶고 카테고리에 저장된 값을 출력하는거니 {}로 묶어주기
        #{self.category_com.post_set.count()} .post_set.count() : .모델명_set(일부만 가져오기) / .count() : 몇개인지 함수로 세기
        self.assertIn(f'{self.category_cul} ({self.category_cul.post_set.count()})', category_card.text)
        self.assertIn(f'미분류 (1)', category_card.text) #test할 때 category 없는 post가 1개이니 (1)이라고 적어주기
   
    def test_post_list(self):
        #1. 
        #post가 있는 경우인 self.assertEqual부터 끝까지를 잘라내서 nav_test뒤로 보내기
        #지금은 post_003까지 있으니 self.assertEqual인자 중 2를 3으로 바꿔주기
        #self.assertIn 인자인 post_001, post_002 등 앞에 self. 붙여주기
        #2.
        #Post가 하나도 안보일 경우일 때는 delete해서 post들을 없애서 테스트해주기
        Post.objects.all().delete()
        #****!!!!!앞서서 response=self.client.get('/body')부터 soup=BeautifulSoup까지 복사해서 하나도 안 보일 때의 경우에 count가 0이다 코드의 뒤에 넣어주기
        #3.
        #nav_test 밑에 다음 코드 작성
        self.category_test(soup) #category_test 만들어주기
```
- sidebar.html
```python
#Categories widget
#5.
<div class="card mb-4" id='category-card'> #id 추가해주기
#<div class="row">밑에 두개의 div로 되어서 두줄로 category가 나타나지만 이를 한 줄로 바꾸고 count를 나타내기
<ul class="list-unstyled mb-0">
	{% for %} #아직 미완성
		<li><a href="#!">Web Design (count)</a></li> #count 코드도 추가하기
	{% endfor %}
        <li><a href="#!">미분류 (count)</a></li>
</ul>
```
- views.py
```python
#7.
from .models import Post, Category

class=PostList(ListView):
    ...
    #sidebar.html에서 미완성된 for문을 완성하기 위해서 다음 코드를 작성해줌 -> count 개수를 넘겨줄 수 있음
    def get_context_data(self, *, object_list=None, **kwargs):
        context=super(PostList, self).get_context_data()
        context['categories']=Category.objects.all() #[] : 템플릿에 필요한 변수 
        context['no_category_post_count']=Post.objects.filter(category=None).count
        return context
```

- sidebar.py
```python
#8.
<div class="card mb-4" id="category-card">
					<div class="card-header">Categories</div>
					<div class="card-body">
						<div class="row">
							<ul class="list-unstyled mb-0">
								{% for c in categories %}
									<li><a href="{{c.get_absolute_url}}">{{c}} ({{c.post_set.count}})</a></li>
								{% endfor %}
									<li><a href="/blog/category/no_category">미분류 ({{no_category_post_count}})</a></li>
							</ul>
						</div>
					</div>
				</div>
```
-cmder
test_post_list만 테스트하기
```
python manage.py test blog.tests.TestView.test_post_list
```

###(2) category 태그 단거 나타내기
- views.py
```python
class PostDetail(DetailView):
    ...
    def get_context_data(self, **kwargs):
        context=super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context
```
- post_list.html
```python
<div class="card-body">
	{% if p.category %}
		<span class="badge badge-secondary float-right">{{p.category}}</span>
	{% else %}
		<span class="badge badge-secondary float-right">미분류</span>
	{% endif %}
```
- post_detail.html
```python
#Post categories
   {% if post.category %}
        <a class="badge bg-secondary text-decoration-none link-light" href="#!">{{post.category}}</a>
   {% else %}
       <a class="badge bg-secondary text-decoration-none link-light" href="#!">미분류</a>
   {% endif %}
```
###(3) url에 category 별로 나타내기 128:800-----/blog/category/카테고리명
- models.py
```python
class Category(models.Model):
    ...
    def get_absolute_url(self):
        return f'/blog/category/{self.slug}'
```
- urls.py
models.py에서 만든 category url 주소를 작성해주기
```python
urlpatterns=[
    ...
    path('category/<str:slug>/', views.category_page) #blog/의 뒤에만 적어주기 / <str:slug> : slug마다 구분을 해야하니 <타입 : 변수>로 작성
                            #views.category_page : 함수이름 가져오기
]
```
- views.py
```python
def category_page(request, slug): #함수작성 / request와 slug 변수도 받으니 slug도 작성
    if slug=='no_category' : #category가 미분류일때 / sidebar.html에서 no_category인자를 전달해서
        category ='미분류'
        post_list = Post.objects.filter(category=None)
    else: #category를 가지고 있을 때
        category=Category.objects.get(slug=slug) #왼쪽 slug : category의 필드명
                                                 #오른쪽 slug : 함수 선언할 때 작성해둔 인자인 slug=url을 통해 전달된 어떤 특정한 값=사용자가 찾기 원하는 값
        post_list=Post.objects.filter(category=category) #왼쪽 category : 위에서 생성한 변수인 category 
    return render(request, 'blog/post_list.html',{
        'category':category,
        'post_list':post_list,
        'categories':Category.objects.all(),
        'no_category_post_count':Post.objects.filter(category=None).count
    })
```
- post_list.html
```python
<h2>Blog
	{% if category %}
		- <span class="badge badge-secondary">{{category}}</span>
	{% endif %}
</h2>
```
### (4) 카테고리별로 링크 연결해주기
- sidebar.html
```python
<ul class="list-unstyled mb-0">
	{% for c in categories %}
	    <li><a href="{{c.get_absolute_url}}">{{c}} ({{c.post_set.count}})</a></li>
	{% endfor %}
		<li><a href="/blog/category/no_category">미분류 ({{no_category_post_count}})</a></li>
</ul>
```
###(5) test
- tests.py
```python
class TestView(TestCase):
    def test_post_detail(self):
        #기존에 만들어둔 post_001은 삭제하고 setUp에 만들어둔 거로 사용하기 위해 self.을 붙여주기
```