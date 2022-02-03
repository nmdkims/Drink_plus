from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import UserModel
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib.auth.decorators import login_required


# 회원가입
def sign_up_view(request):
    if request.method == 'GET':  # GET 메서드로 요청이 들어 올 경우
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signup.html')
    elif request.method == 'POST':  # POST 메서드로 요청이 들어 올 경우
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)
        email = request.POST.get('email', None)

        if password != password2:
            return render(request, 'user/signup.html', {'error': '패스워드를 확인하세여'})
        else:
            if not (username or password):
                return render(request, 'user/signup.html', {'error': '아이디와 패스워드는 필수입니다.'})
            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'user/signup.html', {'error': '중복되는 사용자입니다.'})
            else:
                new_user = UserModel(username=username, password=make_password(password), email=email)
                new_user.save()
                return redirect('/sign-in')


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', "")
        password = request.POST.get('password', "")

        me = auth.authenticate(request, username=username, password=password)
        if me is not None:  # 저장된 유저의 비밀번호와 입력된 비밀번호를 비교
            auth.login(request, me)
            return redirect('/')
        else:
            return render(request, 'user/signin.html', {'error': '아이디 또는 패스워드를 확인해주세요'})  # 로그인 실패시

    elif request.method == 'GET':
        user = request.user.is_authenticated  # 유저가 로그인이 되어있는가 확인
        if user:
            return redirect('/')  # 로그인이 되있을시
        else:  # 되있지 않다면
            return render(request, 'user/signin.html')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')
