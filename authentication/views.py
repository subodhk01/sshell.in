from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login as authLogin, authenticate ,logout as UserLogout
from django.http import HttpResponse
from django.core import exceptions
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from authentication.models import RandomToken
from django.views.generic.edit import FormView
from django.db import transaction, IntegrityError
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django_email_verification import sendConfirm
import urllib


def index(request):
    return render(request, 'index.html')

def forgotpasswordreset(request):
    if request.method == "POST":
        token = ""
        try:
            token = request.POST['token']
            password = request.POST['password']
            password2 = request.POST['password2']
            TokenInstance = get_object_or_404(RandomToken, token=token)
        except KeyError:
            response =  redirect('forgotpasswordreset')
            response['Location'] += "?" + urllib.parse.urlencode({'token':token, 'msg':'Invalid request'})
            return response
        if password != password2:
            response =  redirect('forgotpasswordreset')
            response['Location'] += "?" + urllib.parse.urlencode({'token':token, 'msg':'Passwords do not match'})
            return response
        if len(password) >= 6:
            user = TokenInstance.user
            user.set_password(password)
            user.has_password = True
            user.save()
            TokenInstance.clean()
            response =  redirect('login')
            response['Location'] += "?" + urllib.parse.urlencode({'password_reset':True})
            return response
        else:
            response =  redirect('forgotpasswordreset')
            response['Location'] += "?" + urllib.parse.urlencode({'token':token, 'msg':'Password length should be at least 6 digits'})
            return response
    else:
        token = request.GET.get('token')
        msg = request.GET.get('msg')
        TokenInstance = get_object_or_404(RandomToken, token=token)
        TokenInstance.clean()
        TokenInstance = get_object_or_404(RandomToken, token=token)
        return render(request, 'accounts/forgot_password_reset.html', {'token':token, 'msg':msg})

@require_http_methods(['GET', 'POST'])
@transaction.atomic
def resetpassword(request):
    user = request.user
    if request.method == "POST":
        try:
            has_password = request.POST['has_password']
            print('has_password: ', has_password)
        except KeyError:
            print('KeyError at has_password form field')
            return redirect('index')
        try:
            old_password = request.POST.get('password')
            new_password = request.POST['new_password']
            new_password2 = request.POST['new_password2']
        except KeyError:
            msg = "Missing Fields"
            return render(request, 'accounts/password_reset.html', {'msg':msg,'has_password':has_password })
        if new_password != new_password2:
            msg = "Passwords do not match"
            return render(request, 'accounts/password_reset.html', {'msg':msg, 'has_password':has_password })
        if len(new_password) >= 6:
            if old_password:
                if user.check_password(old_password):
                    user.set_password(new_password)
                    user.save()
                    response = redirect('login')
                    response['Location'] += "?" + urllib.parse.urlencode({'password_reset':True})
                    return response
                else:
                    msg = "Invalid Old Password"
                    return render(request, 'accounts/password_reset.html', {'msg':msg,'has_password':has_password })
            elif not user.has_password:
                user.set_password(new_password)
                user.has_password = True
                user.save()
                response =  redirect('login')
                response['Location'] += "?" + urllib.parse.urlencode({'password_reset':True})
                return response
            else:
                msg = "Missing Old Password"
                return render(request, 'accounts/password_reset.html', {'msg':msg,'has_password':has_password })
        else:
            msg = "Password length should be at least 6 digits."
            return render(request, 'accounts/password_reset.html', {'msg':msg}, {'has_password':has_password })
    else:
        if user.is_authenticated:
            return render(request, 'accounts/password_reset.html', {'has_password':user.has_password})
        else:
            token = get_object_or_404(RandomToken, token=request.GET.get('token'))
            token.clean()
            token = get_object_or_404(RandomToken, token=request.GET.get('token'))
            return render(request, 'accounts/password_reset.html', {
                'has_password':False,
                'token': token.token
            })

def forgotpassword(request):
    if request.method == "POST":
        try:
            detail = request.POST['detail']
        except KeyError:
            msg = "No username or email found"
            return render(request, 'accounts/forgot_password.html', {'msg':msg})
        User = get_user_model()
        try:
            user = User.objects.get(username=detail)
            print(user)
        except User.DoesNotExist:
            try:
                user = get_user_model().objects.get(email=detail)
            except User.DoesNotExist:
                msg = "No User account found with the following detail"
                return render(request, 'accounts/forgot_password.html', {'msg':msg})
        TokenInstance = RandomToken(user=user, expiry_minutes=15)
        TokenInstance.save()
        url = settings.BASE_URL
        url += '/' if not url.endswith('/') else ''
        link = url + "passwordreset/forgotpassword/?" + urllib.parse.urlencode({'token': TokenInstance.token})
        html_message = render_to_string('email/mail_body_forgot_password.html', {'link':link})
        plain_message = strip_tags(html_message)
        mail.send_mail(
            "Reset Password - sshell.in",
            plain_message,
            settings.EMAIL_ADDRESS,
            (user.email,),
            html_message=html_message
        )
        return render(request, 'accounts/forgot_password.html', {'success': True})
    else:
        return render(request, 'accounts/forgot_password.html')

def signupsuccess(request, token):
    TokenInstance = get_object_or_404(RandomToken, token=token)
    TokenInstance.clean()
    TokenInstance = get_object_or_404(RandomToken, token=token)
    email = request.GET.get('email')
    return HttpResponse('Confirmation email sent to you email, checkin the email and login.'+ str(email))

def login(request):
    if request.user.is_authenticated :
        return redirect(index)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            authLogin(request, user)
            return redirect(index)
        else:
            return render(request, 'accounts/login.html', { 'msg': "Invalid Credentials" })
    else:
            return render(request, 'accounts/login.html', {'password_reset': request.GET.get('password_reset')})

@transaction.atomic
def signup(request):
    if request.method == "POST":
        try:
            username = request.POST['username']
            password = request.POST['password']
            password2 = request.POST['password2']
            email = request.POST['email']
        except:
            msg = "Some of the fields are missing."
            return render(request, 'accounts/register.html', { 'msg': msg })
        if len(password) >= 6:
            if password != password2:
                msg = "Entered Passwords do not match"
                return render(request, 'accounts/register.html', { 'msg': msg, 'email':email })
            else:
                try:
                    user = get_user_model().objects.create_user(username, email, password)
                    sendConfirm(user)
                    TokenInstance = RandomToken(user=user, expiry_minutes=20)
                    TokenInstance.save()
                    response = redirect("signupsuccess", token=TokenInstance.token)
                    print(str(response))
                    response['Location'] += "?" + urllib.parse.urlencode({'email':email})
                    return response
                except IntegrityError as e:
                    msg = "Unable to signup, see now this is a problem"
                    if "UNIQUE" in str(e):
                        if 'email' in str(e):
                            msg = "Account with email already exists"
                        elif 'username' in str(e):
                            msg = "Account with Username already exists"
                    return render(request, 'accounts/register.html', { 'msg': msg, 'email':email })
        else:
            msg = "Password length should be at least 6 digits"
            return render(request, 'accounts/register.html', { 'msg': msg, 'email':email })
    else:
        return render(request, 'accounts/register.html')

def logout(request):
    UserLogout(request)
    return redirect(index)