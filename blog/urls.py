from django.urls import path
from . import views

urlpatterns=[
    path('',views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('<int:pk>/new_comment/', views.new_comment),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),
    path('create_post/', views.PostCreate.as_view()),
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('category/<str:slug>/', views.category_page), #IP주소/blog/category/slug/
    path('tag/<str:slug>/', views.tag_page) #IP주소/blog/tag/slug/

    # path('',views.index),  #IP주소/blog  #views 연결하기  #.index : 함수명
    # path('<int:pk>/', views.single_post_page)   #int형으로 옴 , 타입은 pk로,
]