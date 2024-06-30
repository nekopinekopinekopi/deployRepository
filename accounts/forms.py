from django import forms  # ModelFormもこれでいける
from django.contrib.auth.forms import UserCreationForm  # UserCreationFormのベースクラスで二回passwordを入力しそう(使うか迷ってる。一旦ModelFormで行ってみる20240616)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import Users
import re



# ユーザー新規登録
class UserRegistForm(forms.ModelForm):  
    username = forms.CharField(label='ユーザー名')
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput)
    
    
    class Meta:
        model = Users
        fields = ['username', 'email', 'password']


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9]+$', username):
            raise forms.ValidationError('ユーザー名はアルファベットと数字のみ使用できます。')
    
        if Users.objects.filter(username=username).exists():
            raise forms.ValidationError('このユーザー名は既に使われています。')

        return username


    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError('パスワードを入力してください。')
        if len(password) < 8:
            raise forms.ValidationError('パスワードは8文字以上である必要があります。')  # 動作する
        if not re.search(r'[a-zA-Z]', password) or not re.search(r'[0-9]', password):
            raise forms.ValidationError('パスワードにはアルファベットと数字の両方が含まれている必要があります。')  # 動作する
        return password



    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('パスワードが一致しません。')  # 動作する

        return cleaned_data


    def save(self, commit=True):
        user = super().save(commit=False)  # 一旦オブジェクトを作成するが、まだデータベースには保存しない
        user.set_password(self.cleaned_data['password'])  # set_passwordはDjangoのAbstractBaseUserまたはUserモデルにあるメソッドです。パスワードのハッシュ化とパスワードの保存の両方を行います。

        if commit:  # commitがTrueの場合、オブジェクトをデータベースに保存する
            user.save()
        return user  # ハッシュ化されたパスワードを持つユーザーオブジェクトを返す






# ユーザーログイン
class UserLoginForm(AuthenticationForm):  # ログイン時に必要なフィールドを定義する。
    username = forms.CharField(label='ユーザー名')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput)








# ユーザー情報編集
class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(label='ユーザー名')
    email = forms.EmailField(label='メールアドレス')

   
    class Meta:
        model = Users
        fields = ['username', 'email']


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9]+$', username):
            raise forms.ValidationError('ユーザー名はアルファベットと数字のみ使用できます。')
    
        if Users.objects.filter(username=username).exists():
            raise forms.ValidationError('このユーザー名は既に使われています。')

        return username
