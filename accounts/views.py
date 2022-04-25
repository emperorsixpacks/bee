from django.http import Http404
from django.contrib.auth.models import auth
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import EmailMessage
from .forms import UserUpdate, ProfileUpdate


def login_required_active(
        function=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: True if u.is_authenticated and u.userprofile.is_verified else
        False,
        login_url='activate'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            email = request.POST.get('val-email')
            username = request.POST.get('val-username')
            first = request.POST.get('val-first-name')
            last = request.POST.get('val-last-name')
            password = request.POST.get('val-password')
            data = {
                "username": {
                    'username_is_taken': User.objects.filter(username__iexact=username).exists(),
                    'message': 'Username already taken'
                },
                "email": {
                    'email_is_taken': User.objects.filter(email__iexact=email).exists(),
                    'message': 'Email already exists'
                },
                'message': 'Registration successful'
            }
            if data['username']['username_is_taken']:
                messages.error(request, data['username']['message'])
                return redirect('register')

            elif data['email']['email_is_taken']:
                messages.error(request, data['email']['message'])
                return redirect('register')

            else:
                User.objects.create_user(username=username, email=email, first_name=first, last_name=last,
                                         password=password)
                messages.success(request, data['message'])
                # message = render_to_string("success.html")
                # mail = EmailMessage(
                #   subject="Registration successful'",
                #  body=message,
                # from_email='andrewdvd10@gmail.com',
                # to=[email],
                # )
                # mail.content_subtype = 'html'
                # mail.send()
                user = auth.authenticate(username=email, password=password)
                if user is not None:
                    auth.login(request, user)
                    return redirect('dashboard')
        template = 'register.html'
        return render(request, template)


def referral_register(request, code):
    referral_get = get_object_or_404(UserProfile, code=code)
    referral_get_user = User.objects.get(username=referral_get.user)
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            email = request.POST.get('val-email')
            username = request.POST.get('val-username')
            first = request.POST.get('val-first-name')
            last = request.POST.get('val-last-name')
            password = request.POST.get('val-password')
            data = {
                "username": {
                    'username_is_taken': User.objects.filter(username__iexact=username).exists(),
                    'message': 'Username already taken'
                },
                "email": {
                    'email_is_taken': User.objects.filter(email__iexact=email).exists(),
                    'message': 'Email already exists'
                },
                'message': 'Registration successful'
            }
            if data['username']['username_is_taken']:
                messages.error(request, data['username']['message'])
                return redirect('referral', code=code)

            elif data['email']['email_is_taken']:
                messages.error(request, messages.error(request, data['email']['message']))
                return redirect('referral', code=code)

            else:
                x = User.objects.create_user(username=username, email=email, first_name=first, last_name=last,
                                             password=password)
                UserProfile.objects.filter(user__username=x).update(referral=referral_get_user)
                referral_get.first_gen.add(x)
                if referral_get.referral:
                    get_top = UserProfile.objects.get(user=referral_get.referral)
                    get_top.second_gen.add(x)
                    print(get_top)

                print(x)
                print(referral_get.first_gen.all())

                print(referral_get.first_gen.all())
                messages.success(request, data['message'])
                # message = render_to_string("success.html")
                # mail = EmailMessage(
                #   subject="Registration successful'",
                #  body=message,
                # from_email='andrewdvd10@gmail.com',
                # to=[email],
                # )
                # mail.content_subtype = 'html'
                # mail.send()
                user = auth.authenticate(username=email, password=password)
                if user is not None:
                    auth.login(request, user)
                    return redirect('dashboard')
        template = 'register.html'
        return render(request, template)


def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            print(email)
            password = request.POST.get('password')
            user = auth.authenticate(username=email, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')

            else:
                messages.info(request, 'invalid username or password')
                return redirect('login')
        template = 'login.html'
        return render(request, template)


@login_required(login_url='login')
def deactivate_and_activate_url(request):
    user = UserProfile.objects.get(user=request.user)
    if user.is_verified:
        raise Http404
    else:
        template = 'activate.html'
        return render(request, template)


@login_required
def logout(request):
    auth.logout(request)
    messages.info(request, 'Logged out')
    return redirect('login')


@login_required_active()
@login_required()
def settings(request):
    if request.method == 'POST':
        form = UserUpdate(request.POST, instance=request.user)
        form2 = ProfileUpdate(request.POST, request.FILES, instance=request.user.userprofile)

        if form2.is_valid() and form2.is_valid():
            obj = form2.save()
            print(obj.profile_pic)
            messages.success(request, 'Profile updated')
            return redirect('settings')
    else:
        form = UserUpdate(instance=request.user)
        form2 = ProfileUpdate(instance=request.user.userprofile)
    template = 'settings.html'
    return render(request, template, {'form': form, 'form2': form2})
