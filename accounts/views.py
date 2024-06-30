from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from django.views.generic import (
    TemplateView, CreateView, DetailView, UpdateView
)
from .forms import (
    UserRegistForm, UserLoginForm, UserUpdateForm,
)
from .models import Users
import os




# welcomeページ表示
class WelcomeView(TemplateView):
    template_name = os.path.join('accounts', 'welcome.html')
    
    
# 新規登録ページ表示
class UserRegistView(CreateView):
    form_class = UserRegistForm
    template_name = os.path.join('accounts', 'user_regist.html')
    success_url = reverse_lazy('accounts:login')  # app_name定義してるからこうやって記述しなきゃだ！
    

# ログインページ
class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = os.path.join('accounts', 'login.html')
    redirect_authenticated_user = True
    
    
    
# ログアウト処理
class UserLogoutView(LoginRequiredMixin, LogoutView):
    pass  # LOGOUT_REDIRECT_URLをsettings.pyに定義してます。


    
# ユーザー情報ページ
class UserDetailView(LoginRequiredMixin, DetailView):
    model = Users
    context_object_name = 'user_detail'
    template_name = 'accounts/user_detail.html'

    def get_object(self):  # ログイン中のユーザーを呼び出してます
        return self.request.user
    
    # ↑ずっとNoReverseMatchのエラーが出てて。urlsには<int:pk>が必須だと思ってたら、viewsとかhtmlとかと話が合わなかったみたいで、urlのint消したらいけた。
    
  

        
#ユーザー更新ページ
class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    template_name = os.path.join('accounts', 'user_update.html')
    success_url = reverse_lazy('accounts:user_detail')
    
    def get_object(self):  # ログイン中のユーザーを呼び出してます
        return self.request.user
