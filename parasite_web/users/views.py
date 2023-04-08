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
# Login User
def loginUser(request): 
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password1']
        if email is not None and password is not None:
            try: 
                user = User.objects.get(email=email)
                if user.is_active and user.password==password:
                    return redirect('/game/')
                elif user.password!=password:
                    error = 'You entered an incorrect email or password'
                else: 
                    error = "Your account is not activated. Please click the activation button we have sent to your email"
                form = LoginForm()
                return render(request, 'login.html', {'form': form, 'error': error})
            except: 
                form = LoginForm()
                return render(request, 'login.html', {'form': form, 'error': 'You entered an incorrect email or password'})
        else: 
            form = LoginForm()
            return render(request, 'login.html', {'form': form, 'error': 'You need to introduce a registered email and a password'})
    else: 
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

# Activate user in DB when the activation button is clicked
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
        title = "Activation Link Error"
        message = "Activation link has expired or another error occurred. Please try again later."
        return redirect(f'/users/error?title={title}&message={message}')

# Send email to the user to activate account
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

# Register a user (inactive by default) 
def registerUser(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User(first_name = form.cleaned_data.get("first_name"),
                        last_name = form.cleaned_data.get("last_name"),
                        email = form.cleaned_data.get("email"),
                        password = form.cleaned_data.get("password1")
                        )
            try: 
                user.save()
                status = activateEmail(request, user, form.cleaned_data.get("email"))
                if status:
                    return render(request, 'register-email.html', {'email': form.cleaned_data.get("email")})
                else: 
                    title = "Sending Email Error"
                    message = "We were not able to send you the confirmation email. Please try again later."
                    return redirect(f'/users/error?title={title}&message={message}')
            except: 
                form = SignUpForm()
                return render(request, 'signup.html', {'form': form, 'error': 'This email is already registered. Please use another email to sign up.'})
        else: 
            form = SignUpForm()
            return render(request, 'signup.html', {'form': form, 'error': 'The data you introduced was invalid. Your errors are: ' + str(form.errors)})
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

# Change the password of a user
def forgotPassword(request): 
    if request.method == 'POST':
        email = request.POST['email']
        if email is not None:
            try: 
                user = User.objects.get(email=email)
                return render(request, 'check-email.html')
            except:
                form = EmailForm()
                return render(request, 'forgot-password.html', {'form': form, 'error': 'You need to introduce a registered email'})
        else: 
            form = EmailForm()
            return render(request, 'forgot-password.html', {'form': form, 'error': 'You need to introduce a registered email'})
    else: 
        form = EmailForm()
        return render (request, 'forgot-password.html', {'form': form})

# Display errors
def error(request):
    title = request.GET.get('title')
    message = request.GET.get('message')
    return render(request, 'error.html', {'title': title, 'message': message})