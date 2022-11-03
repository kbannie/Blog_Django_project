#테스트
##1. cmder
```
pip install beautifulsoup4
python manage.py test
```
##2. tests.py
###(2) tests.py
```py
from django.test import TestCase, Client  #추가한 코드 : Client
from bs4 import BeautifulSoup
from .models import Post #사용하는 Post 모델

class TestView(TestCase): #대문자로 시작하는 클래스명/ ()안에 있는 것을 상속받음
    def setUp(self): #setUp : 함수들이 공통적으로 필요한 것 = client 정보
        self.client=Client() #client : 매개변수 / 상단에 Client를 import해주기
    
    def nav_test(self, soup): #navbar 따로 빼주기 #soup변수를 받으니 이것도 인자로 넣어주기
        navbar=soup.nav #변수 선언 가능
        self.assertIn('Blog',navbar.text) #assertIn : <nav>태그에 Blog가 있는지 확인 #Blog, AboutMe등 html파일에서 적은 것과 같은 거를 적어야함
        self.assertIn('AboutMe',navbar.text)
        
    def test_post_list(self):
        response=self.client.get('/blog/') #/blog/에 있는 코드가 response에 전달됨
        
        #respnse 결과가 정상적인지 확인
        self.assertEqual(response.status_code, 200) #assertEqual:()안의 인자가 같은지
        soup=BeautifulSoup(response.content, 'html.parser') #response.content를 BeautifulSoup이 분석하고 이를 html로 파서하기
        
        #title이 정상적으로 보이는지
        self.assertEqual(soup.title.text, 'Blog') #assertEqual : 두 인자가 같은지 확인#<title>Blog</title> 처럼 <title>태그 안에 있는 코드/ .text : <title>태그 안의 코드만 가져오기
        
        #navbar가 정상적으로 보이는지
        # navbar=soup.nav #변수 선언 가능
        # self.assertIn('Blog',navbar.text) #assertIn : <nav>태그에 Blog가 있는지 확인 #Blog, AboutMe등 html파일에서 적은 것과 같은 거를 적어야함
        # self.assertIn('AboutMe',navbar.text)
        self.nav_test(soup) #위에서 nav_test()에 위 3줄 코드를 넣어 함수로 묶고 이를 본문에서 불러오기 
        # test_post_list에서 soup 변수를 선언해주어서 nav_test는 soup을 읽을 수 없음->soup을 변수를 전달하기
        
        #Post가 정상적으로 보이는지
        #1. 맨 처음엔 Post가 하나도 안보임
        self.assertEqual(Post.objects.count(),0)
        main_area=soup.find('div',id="main-area") #div태그들 중에서 id가 main-area인 태그를 찾기
        self.assertIn('아무 게시물이 없습니다.', main_area.text)  
        #post_list.html 수정필요
        #{% for p in post_list %} 앞에 {% if post_list.exists %}써주어서 post_list가 있을 때 반복문을 실행
        #{% endfor %} 뒤에 {% else %} <h5>아무 게시물이 없습니다.</h5> {% endif %}
        #(주 내용을 감싸는 태그)=> <div class="col-md-8 col-lg-9"> 태그 안에 id="main-area" 작성
        
        #2. Post가 있는 경우
        post_001=Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다.") #blank=True라고 적인 필드는 생략 가능
        post_002=Post.objects.create(title="두번째 포스트", content="두번째 포스트입니다.")
        self.assertEqual(Post.objects.count(),2)
        
        #다시 처음부터 해주기
        response=self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup=BeautifulSoup(response.content, 'html.parser')
        main_area=soup.find('div',id="main-area")
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        self.assertNotIn('아무 게시물이 없습니다.', main_area.text)

    def test_post_detail(self):
        post_001=Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다.") #적어도 하나의 포스트가 존재해야 detail 확인이 가능
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

        response=self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup=BeautifulSoup(response.content, 'html.parser')
        
        #navbar가 정상적으로 보이는지
        # navbar=soup.nav
        # self.assertIn('Blog',navbar.text)
        # self.assertIn('AboutMe',navbar.text)
        self.nav_test(soup)
        #post_list.html 수정필요
        #nav태그에서 Blog, AboutMe 있는지 확인하고 없으면 수정하기

        self.assertIn(post_001.title, soup.title.text)
        #post_detail.html 수정필요
        #(주 내용을 감싸는 태그)=> <div class="col-md-8"> 태그 안에 id="main-area" 작성
        #article 태그를 div 태그로 바꾸고 id="post-area" 작성  
        #section 태그를 div 태그로 바꾸고 id="comment-area" 작성  => div로 통일시키기 위해
        #title부분에 {{post.title}}로 되어 있어야 함

        main_area=soup.find('div', id='main-area')
        post_area=main_area.find('div', id="post-area")  #main_area에서 찾으면 되니 soup이 아닌 main_area로 작성
        self.assertIn(post_001.title, post_area.text)
        self.assertIn(post_001.content, post_area.text) #create할 때, title과 content 넣어주었으니
```
