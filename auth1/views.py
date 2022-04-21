from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, LoginForm, AccountUpdateForm
from .models import RegisterUser

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
    context = {}
    profile = RegisterUser.objects.get(id=request.user.id)
    context['profile'] = profile
    return render(request, 'auth1/profile.html', context)

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


