from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from cadastro.forms import RegistrationForm, AuthenticateContaForm, ContaUpdateForm


def registration_view(request, date_of_birth=None):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email= form.cleaned_data.get('email')
            data_of_birth = form.cleaned_data.get('date_of_birth')
            raw_password = form.cleaned_data.get('password1')
            cadastro= authenticate(email=email, date_of_birth= date_of_birth,  password=raw_password,)
            login(request, cadastro)
            return redirect('home')
        else:
            context['registration_form'] = form
    else:  # GET request
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'register.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = AuthenticateContaForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

        if user:
            login(request, user)
            return redirect("home")

    else:
        form = AuthenticateContaForm()

    context['login_form'] = form

    return render(request, 'login.html', context)


def conta_view(request):

    if not request.user.is_authenticated:
            return redirect("login")

    context = {}

    if request.POST:
            form = ContaUpdateForm(request.POST, instance = request.user)
            if form.is_valid():
                form.initial = {
                    "email": request.POST['email'],
                    "username": request.POST['username'],
                }
                form.save()
                context['success_message'] = "Atualizado"

    else:
            form = ContaUpdateForm(
                        initial= {
                                    "email": request.user.email,
                                    "username": request.user.username,
                        }
            )
    context['conta_form'] = form
    return render(request, 'conta.html', context)

