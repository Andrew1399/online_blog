from django.urls import path
from posts.views import (HomeView,
    PostView, PostCreateView, PostUpdateView, PostDeleteView,
    LikeView, SearchPostView, CategoryView)
from posts import views

app_name = 'posts'


urlpatterns = [
    path('post_page/', HomeView.as_view(), name='post_page'),
    path('post/<pk>/<slug:slug>', PostView.as_view(), name='post'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('like/<int:pk>', LikeView, name='like'),
    path('search/', SearchPostView.as_view(), name='search'),
    path("category/<str:cats>/", CategoryView, name='category')
]
