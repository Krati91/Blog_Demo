from django.urls import path,re_path
from . import views

urlpatterns = [
    path('', views.home_view, name="home"),
    path('login',views.login_view, name="login"),
    path('register', views.register_view, name="register"),
    path('user_created',views.create_user_view, name="create_user"),
    path('user_account',views.user_account_view, name="user_account"),
    path('logout',views.logout_view, name="logout"),
    path('new_blog',views.add_new_blog_view,name="add_new_blog"),
    re_path(r'^api/search/', views.autocompleteModel, name='search'),
    path('user_profile', views.user_profile_view, name='user_profile'),
]    