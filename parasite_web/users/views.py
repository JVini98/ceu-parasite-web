from django.shortcuts import render, HttpResponse, redirect
from .forms import SignUpForm, LoginForm, EmailForm, PasswordForm
from .models import User
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .token import account_activation_token

import urllib.parse

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
                    error = 'You entered an incorrect email or password.'
                else: 
                    error = "Your account is not activated. Please click the activation button we have sent to your email."
                form = LoginForm()
                return render(request, 'login.html', {'form': form, 'error': error})
            except: 
                form = LoginForm()
                return render(request, 'login.html', {'form': form, 'error': 'You entered an incorrect email or password.'})
        else: 
            form = LoginForm()
            return render(request, 'login.html', {'form': form, 'error': 'You need to introduce a registered email and a password.'})
    else: 
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

# Activate user in DB when the activation button is clicked
# or Change password in DB when the reset button is clicked
def verifyLink(request, uidb64, token, action):
    try: 
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except: 
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        if action == "Activate":
            user.is_active = True
            user.save()
            return redirect('/users/')
        elif action == "Reset":
            encoded_email= urllib.parse.quote(user.email)
            request.session['encoded_email'] = encoded_email
            return redirect('/users/reset_password')
    else: 
        title = "Activation Link Error"
        message = "Activation link has expired or another error occurred. Please try again later."
        return redirect(f'/users/error?title={title}&message={message}')

# Send email to the user to activate account or reset password
def activateEmail(request, user, email, subject):
    if subject=="Activate":
        mail_subject = "Activate your account"
        template= "activate-account.html"
    elif subject=="Reset":
        mail_subject = "Reset your password"
        template= "password-email.html"
    message = render_to_string(template,{
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "domain": get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'action': subject,
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[email])
    email.content_subtype='html'
    if email.send():
        return True
    else:
        return False

# Check if user is valid
def checkUser(form):
    if (form.cleaned_data.get("password1")==form.cleaned_data.get("password2")):
        user = User(first_name = form.cleaned_data.get("first_name"),
                    last_name = form.cleaned_data.get("last_name"),
                    email = form.cleaned_data.get("email"),
                    password = form.cleaned_data.get("password1")
                    )
        if (User.objects.filter(email=user.email).exists()):
            return [False, None, "Email"]
        else:
            user.save()
            return [True, user, None]
    else: 
        return [False, None, "Password"]

# Register a user (inactive by default) 
def registerUser(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            valid, user, error = checkUser(form)
            if valid: 
                status = activateEmail(request, user, form.cleaned_data.get("email"), "Activate")
                if status:
                    return render(request, 'register-email.html', {'email': form.cleaned_data.get("email")})
                else: 
                    title = "Sending Email Error"
                    message = "We were not able to send you the confirmation email. Please try again later."
                    return redirect(f'/users/error?title={title}&message={message}')
            else: 
                if error=="Email":
                    return render(request, 'signup.html', {'form': form, 'error': 'This email is already registered. Please use another email to sign up.'})
                elif error=="Password":
                    return render(request, 'signup.html', {'form': form, 'error': 'The passwords do not match. Plase make sure you typed them correctly.'})
        else: 
            form = SignUpForm()
            return render(request, 'signup.html', {'form': form, 'error': 'The data you introduced was invalid. Your errors are: ' + str(form.errors)})
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

# User requests a new password
def forgotPassword(request): 
    if request.method == 'POST':
        email = request.POST['email']
        if email is not None:
            try: 
                user = User.objects.get(email=email)
                status = activateEmail(request, user, email, "Reset")
                if status: 
                    return render(request, 'check-email.html', {'email': email})
                else: 
                    title = "Sending Email Error"
                    message = "We were not able to send you the reset password email. Please try again later."
                    return redirect(f'/users/error?title={title}&message={message}')
            except:
                form = EmailForm()
                return render(request, 'forgot-password.html', {'form': form, 'error': 'You need to introduce a registered email.'})
        else: 
            form = EmailForm()
            return render(request, 'forgot-password.html', {'form': form, 'error': 'You need to introduce a registered email.'})
    else: 
        form = EmailForm()
        return render (request, 'forgot-password.html', {'form': form})
    
# Change a user password
def resetPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        if (pass1 == pass2):
            try: 
                user = User.objects.get(email=email)
                user.password = pass1
                user.save()
                return redirect('/users/')
            except: 
                form = PasswordForm()
                error = "The email account is not registered." + str(user)
                return render(request, 'reset-password.html', {'form': form, 'error': error})    
        else: 
            form = PasswordForm()
            error = "The passwords do not match. Plase make sure you typed them correctly."
            return render(request, 'reset-password.html', {'form': form, 'error': error}) 
    else: 
        decoded_email = urllib.parse.unquote(request.session.get('encoded_email'))
        del request.session['encoded_email']
        form = PasswordForm()
        return render(request, 'reset-password.html', {'form': form, 'email': decoded_email}) 

# Display errors
def error(request):
    title = request.GET.get('title')
    message = request.GET.get('message')
    return render(request, 'error.html', {'title': title, 'message': message})