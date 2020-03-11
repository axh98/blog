from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserLoginForm(forms.Form):
    #      forms.Form    适用于不与数据库进行直接交互，用户登录不需要对数据库进行改动
    #      需要手动配置每个字段
    username = forms.CharField()
    password = forms.CharField()


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField()
    password1 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email')

    # clean_   这种写法     django   会自动调用   检查   clean   后面的字段
    def clean_password1(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password1'):
            return data.get('password')
        else:
            raise forms.ValidationError('两次输入密码不一致，请重试')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'bio')
