from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login as authLogin, authenticate ,logout as UserLogout
from django.http import HttpResponse
from django.core import exceptions
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from authentication.models import RandomToken, Contact
from django.views.generic.edit import FormView
from django.db import transaction, IntegrityError
from django.core import mail
from django.utils import timezone
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
            response['Location'] += "?" + urllib.parse.urlencode({'f':True})
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
        return redirect('dashboard')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            authLogin(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'accounts/login.html', { 'msg': "Invalid Credentials" })
    else:
        print(request.GET.get('password_reset'))
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
                    user.last_send_verification_link = timezone.now()
                    user.save()
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

@login_required
def emailnotverified(request):
    if request.user.is_verified:
        return redirect('dashboard')
    time = timezone.now()
    diff = time - request.user.last_send_verification_link
    print(diff.seconds)
    if diff.seconds < 300:
        return render(request, 'accounts/email_not_verified.html', {
            'wait':True,
            'time':300 - diff.seconds
        })
    if request.method == "POST":
        user = request.user
        sendConfirm(user)
        user.last_send_verification_link = timezone.now()
        user.save()
        TokenInstance = RandomToken()
        TokenInstance.save()
        msg = "Confirmation Email successfully sent, check your email."
        return redirect('success', token=TokenInstance.token, msg=msg)
    return render(request, 'accounts/email_not_verified.html', {
        'wait':False
    })

def team(request):
    return render(request, 'team.html')

def privacypolicy(request):
    return render(request, 'privacypolicy.html')


def contact(request):
    if request.method == "POST":
        try:
            name = request.POST['name']
            email = request.POST['email']
            phone = request.POST['phone']
            message = request.POST['message']
        except:
            msg = "Missing Fields"
            return render(request, 'contact.html', { 'msg':msg })
        contact = Contact(
            name=name,
            email=email,
            phone_number=phone,
            message=message
        )
        contact.save()
        TokenInstance = RandomToken()
        TokenInstance.save()
        msg = "Thank you for contacting us, we will reach you soon."
        return redirect('success', token=TokenInstance.token, msg=msg)
        
    return render(request, 'contact.html')

def success(request, token, msg):
    TokenInstance = get_object_or_404(RandomToken, token=token)
    TokenInstance.clean()
    TokenInstance = get_object_or_404(RandomToken, token=token)
    TokenInstance.delete()
    return render(request, 'success.html', {'msg':msg})

def logout(request):
    UserLogout(request)
    return redirect(index)