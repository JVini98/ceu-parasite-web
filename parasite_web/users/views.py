from django.shortcuts import render, HttpResponse, redirect
from .forms import SignUpForm, LoginForm, EmailForm
from .models import User
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .token import account_activation_token

# Create your views here.
def loginUser(request): 
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password1']
        if email is not None and password is not None:
            user = User.objects.get(email=email)
            if user.is_active:
                return redirect('/game/')
            else: 
                return HttpResponse("Your account is not activated. Please click the activation button we have send you to your email.")
        else: 
            # throw an error
            id = User.objects.get(email=form.cleaned_data["email"])
            return HttpResponse("No ha ido bien la validación " + str(id))
    else: 
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def activate(request, uidb64, token):
    try: 
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except: 
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('/users/')
    else: 
        return HttpResponse("Activation link has expired or another error occurred. Please try again.")

def activateEmail(request, user, email):
    mail_subject = "Activate your account"
    message = render_to_string("activate-account.html",{
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "domain": get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[email])
    email.content_subtype='html'
    if email.send():
        return True
    else:
        return False

def registerUser(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User(first_name = form.cleaned_data.get("first_name"),
                        last_name = form.cleaned_data.get("last_name"),
                        email = form.cleaned_data.get("email"),
                        password = form.cleaned_data.get("password1")
                        )
            user.save()
            status = activateEmail(request, user, form.cleaned_data.get("email"))
            if status:
                return render(request, 'register-email.html', {'email': form.cleaned_data.get("email")})
            else: 
                return HttpResponse("No ha ido bien el envio del correo")
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