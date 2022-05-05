from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.conf import settings
from datetime import date
# from post.models import Post
# from post.forms import PostForm
from .forms import RegistrationForm, LoginForm, AccountUpdateForm
from .models import RegisterUser, Notification

def loginUserView(request):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('home')
    
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('home')

    else:
        form = LoginForm()
    
    context['login_form'] = form
    return render(request, 'auth1/login.html', context)

def registerUserView(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1') #No changes for fixing pass fields in amdin
            account = authenticate(email=email, password=raw_password)
            login(request, account)

            # Send email for new registration
            # subject = "Account created successfuly"
            # message = f" Hey {request.user.name}, your account was created successfuly. Click http://127.0.0.1:8000/ to continue to visit Blood Donor System"
            # recipient = f"{request.user.email}"
            # send_mail(
            #     subject,
            #     message,
            #     settings.EMAIL_HOST_USER,
            #     [recipient],
            #     fail_silently = False
            # )

            return redirect('home')
            
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'auth1/register.html', context)


def logoutUserView(request):
    logout(request)
    return redirect('home')

def profileUserView(request):

    profile = RegisterUser.objects.get(id=request.user.id)

    born = request.user.date_of_birth
    today = date.today()
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    return render(request, 'auth1/profile.html', {
        'profile': profile,
        'age': age,
    })


def updateProfileView(request):

    if not request.user.is_authenticated:
        return redirect('logoutUserView')

    context = {}
    
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect('profileUser')
    else:
        form = AccountUpdateForm(
            initial = {
                "email": request.user.email,
                "username": request.user.username,
                "name": request.user.name,
                "contact_number": request.user.contact_number,
                "address": request.user.address,
                "date_of_birth": request.user.date_of_birth,
                "nid": request.user.nid,
                "blood_group": request.user.blood_group,
            }
        )
            
    context['form'] = form
    return render(request, 'auth1/update_profile.html', context)


def view_notifications(request, pk):
    user = request.user.id
    notifications = Notification.objects.filter(receiver=user)
    unread_notifications = Notification.objects.filter(receiver=user).exclude(read_by=user)
    total_unread_notifications = len(unread_notifications)
    return render(request, 'auth1/notifications.html', {
        'notifications': notifications,
        'total_unread_notifications': total_unread_notifications,
    })

def mark_as_read(request, pk):
    user = RegisterUser.objects.filter(pk=request.user.id)
    notification = Notification.objects.get(id=pk)
    notification.read_by.set(user)
    return redirect(f"/posts/view/{notification.context}")

def handle_404(request, exception):
    return render(request, 'auth1/404.html')