from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .forms import RegisterUserForm, EditProfileForm, FormChangePassword
from django.contrib.auth.decorators import login_required


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.GET:
                return redirect(request.GET['next'])  # does it work?!?!?!?!?
            else:
                return redirect('films:index')
        else:
            messages.success(request, "Error! You've entered wrong username or password!")
            return redirect("login")

    else:
        return render(request, 'authenticate/login.html', {})


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.success(request, "You were logged out!")
    return redirect("films:index")


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("films:index")
    else:
        form = RegisterUserForm()

    return render(request, 'authenticate/register.html', {'form': form})


@login_required(login_url='login')
def profile(request):
    context = {'user': request.user}
    return render(request, 'authenticate/profile.html', context)


@login_required(login_url='login')
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been edited!")
            return redirect('profile')
        else:
            messages.success(request, "There was an error with your form!")
            return redirect('edit')

    else:
        form = EditProfileForm(instance=request.user)
        return render(request, 'authenticate/edit_profile.html', {'form': form})


@login_required(login_url='login')
def change_password(request):
    if request.method == "POST":
        form = FormChangePassword(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Successful password change!")
            return redirect('profile')
        else:
            messages.success(request, "There was an error!")
            return redirect('change_password')
    else:
        form = FormChangePassword(user=request.user)
        return render(request, 'authenticate/change_password.html', {'form': form})
