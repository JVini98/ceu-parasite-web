from django.shortcuts import render, HttpResponse, redirect
from .forms import SignUpForm, LoginForm, EmailForm
from .models import User

# Create your views here.
def loginUser(request): 
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password1']
        if email is not None and password is not None:
            id = str(User.objects.get(email=email))
            #return render(request, 'game.html', {'id': id})
            return redirect('/game/')
        else: 
            # throw an error
            id = User.objects.get(email=form.cleaned_data["email"])
            return HttpResponse("No ha ido bien la validación " + str(id))
    else: 
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def registerUser(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            # user = User(first_name = form.cleaned_data.get("first_name"),
            #             last_name = form.cleaned_data.get("last_name"),
            #             email = form.cleaned_data.get("email"),
            #             password = form.cleaned_data.get("password1")
            #             )
            #user.save()
            return render(request, 'register-email.html', {'email': form.cleaned_data.get("email")})
            #return render(request, 'login.html', {'form': LoginForm()})
        else: 
            #throw an error
            return HttpResponse("El error es " + str(form.errors))
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

def forgotPassword(request): 
    if request.method == 'POST':
        email = request.POST['email']
        if email is not None:
            id = str(User.objects.get(email=email))
            return render(request, 'check-email.html')
        else: 
            return HttpResponse("No ha ido bien la validación")
    else: 
        form = EmailForm()
        return render (request, 'forgot-password.html', {'form': form})