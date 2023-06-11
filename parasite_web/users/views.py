from django.shortcuts import render, HttpResponse, redirect
from .forms import SignUpForm, LoginForm, EmailForm, PasswordForm
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage, send_mail
from .token import account_activation_token
from django.conf import settings

import urllib.parse
import threading

# Create your views here.
# Login User
def loginUser(request): 
    # POST method
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password1']
        # Check the form is not empty
        if email is not None and password is not None:
            # Try to find the user in the DB
            try: 
                user = User.objects.get(email=email)
                # The account is activated and the password is correct
                if user.is_active and check_password(password, user.password):
                    request.session['user']=email
                    return redirect('/')
                # The password is incorrect
                elif not check_password(password, user.password):
                    error = 'You entered an incorrect email or password.'
                # The account is not activated
                else: 
                    error = "Your account is not activated. Please click the activation button we have sent to your email."
            # User not found in the DB
            except: 
                error = 'You entered an incorrect email or password.'
        # The form is empty
        else: 
            error = "You need to introduce a registered email and a password"
        form = LoginForm()
        return render(request, 'login.html', {'form': form, 'error': error})
    # GET Method mainly
    else: 
        # If the user is logged in, display an error
        if ('user' in request.session):
            error = 'To log in with another account, please log out first'
            return redirect(f'/?error={error}')
        # Allow the user to log in
        else: 
            # The user changed the password and it is redirected to login
            if request.session.get('password_succes'):
                message = request.session.get('password_succes')
                del request.session['password_succes']
                form = LoginForm()
                return render(request, 'login.html', {'form': form, 'message': message})
            # Without any session variables
            else: 
                form = LoginForm()
                return render(request, 'login.html', {'form': form})

# Activate user in DB when the activation button is clicked
# or allow to change password when the reset button is clicked
def verifyLink(request, uidb64, token, action):
    # Try to get the user matching the received UID
    try: 
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except: 
        user = None
    
    # The user was found in the DB and the token is correct
    if user is not None and account_activation_token.check_token(user, token):
        # Activate account of the user
        if action == "Activate":
            user.is_active = True
            user.save()
            return redirect('/users/')
        # Allow to reset the password of the user
        elif action == "Reset":
            encoded_email= urllib.parse.quote(user.email)
            request.session['encoded_email'] = encoded_email
            return redirect('/users/reset_password')
    # The main issue is that the activation link has already expired
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
        template= "activate-password.html"
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
    # Send it async
    threading.Thread(target=send_mail, args=(mail_subject, message, settings.EMAIL_FROM, [email]), kwargs={'fail_silently': True, 'html_message': message}).start()
    # Send it sync
    # email = EmailMessage(mail_subject, message, to=[email])
    # email.content_subtype='html'
    # if email.send():
    #     return True
    # else:
    #     return False

# Check if user is valid
def checkUser(form):
    # Checks to perform when registration
    if (form.cleaned_data.get("password1")==form.cleaned_data.get("password2")):
        user = User(first_name = form.cleaned_data.get("first_name"),
                    last_name = form.cleaned_data.get("last_name"),
                    email = form.cleaned_data.get("email"),
                    password = make_password(form.cleaned_data.get("password1"))
                    )
        # There is an existing user with that email
        if (User.objects.filter(email=user.email).exists()):
            return [False, None, "Email"]
        # Everything is correct and the user is saved in DB
        else:
            user.save()
            return [True, user, None]
    # Passwords do not match at the Server
    else: 
        return [False, None, "Password"]

# Register a user (inactive by default) 
def registerUser(request):
    # POST method
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # If the form (data sent by the user) is valid
        if form.is_valid():
            valid, user, error = checkUser(form)
            # If all the checks of the user were alright
            if valid: 
                # status = activateEmail(request, user, form.cleaned_data.get("email"), "Activate")
                activateEmail(request, user, form.cleaned_data.get("email"), "Activate")
                return render(request, 'email-activate.html', {'email': form.cleaned_data.get("email")})
                # The email was successfully sent to the user
                # if status:
                #     return render(request, 'email-activate.html', {'email': form.cleaned_data.get("email")})
                # # The email was not sent to the user
                # else: 
                #     title = "Sending Email Error"
                #     message = "We were not able to send you the confirmation email. Please try again later."
                #     return redirect(f'/users/error?title={title}&message={message}')
            # Display the error that happen during registration
            else: 
                if error=="Email":
                    error = "This email is already registered. Please use another email to sign up."
                elif error=="Password":
                    error = "The passwords do not match. Plase make sure you typed them correctly."
                return render(request, 'signup.html', {'form': form, 'error': error})
        # The form was invalid
        else: 
            form = SignUpForm()
            return render(request, 'signup.html', {'form': form, 'error': 'The data you introduced was invalid. Your errors are: ' + str(form.errors)})
    # GET method mainly
    else:
        # If the user is logged in, display an error
        if ('user' in request.session):
            error = 'To register another account, please log out first'
            return redirect(f'/?error={error}')
        # Allow the user to register
        else: 
            form = SignUpForm()
            return render(request, 'signup.html', {'form': form})

# User requests a new password
def forgotPassword(request): 
    # POST method
    if request.method == 'POST':
        email = request.POST['email']
        # Check if an email was received
        if email is not None:
            # Try to find that user register in the DB
            try: 
                user = User.objects.get(email=email)
                activateEmail(request, user, email, "Reset")
                return render(request, 'email-password.html', {'email': email})
                # status = activateEmail(request, user, email, "Reset")
                # # The email was successfully sent to the user
                # if status: 
                #     return render(request, 'email-password.html', {'email': email})
                # # The email was not sent to the user
                # else: 
                #     title = "Sending Email Error"
                #     message = "We were not able to send you the reset password email. Please try again later."
                #     return redirect(f'/users/error?title={title}&message={message}')
            except:
                error = "You need to introduce a registered email."
        # There was no email received
        else: 
            error='You need to introduce a registered email.'
        form = EmailForm()
        return render(request, 'forgot-password.html', {'form': form, 'error': error})
    # GET method mainly
    else: 
        # If the user is logged in, display an error
        if ('user' in request.session):
            error = 'To change the password of an account, please log out first'
            return redirect(f'/?error={error}')
        # Allow the user to introduce their email change the password 
        else: 
            form = EmailForm()
            return render (request, 'forgot-password.html', {'form': form})
    
# Change a user password
def resetPassword(request):
    # POST method
    if request.method == 'POST':
        email = request.POST['email']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        # Check if passwords match
        if (pass1 == pass2):
            # Try to find the user in the DB who requested the change
            try: 
                user = User.objects.get(email=email)
                user.password = make_password(pass1)
                user.save()
                request.session['password_succes'] = "Your password was successfully changed"
                return redirect('/users/')
            # User not found
            except: 
                error = "The email account is not registered."   
        # Password do not match
        else: 
            error = "The passwords do not match. Plase make sure you typed them correctly."
        form = PasswordForm()
        return render(request, 'reset-password.html', {'form': form, 'error': error}) 
    # GET method
    else: 
        # Change the password through the email
        if request.session.get('encoded_email'):
            decoded_email = urllib.parse.unquote(request.session.get('encoded_email'))
            del request.session['encoded_email']
            form = PasswordForm()
            return render(request, 'reset-password.html', {'form': form, 'email': decoded_email})
        # Change the password through other means
        else: 
            title = "Change your password through the email link"
            message = "You need to change your password through the email link, otherwise, you will not be allow to do so."
            return redirect(f'/users/error?title={title}&message={message}')

# Display errors
def error(request):
    title = request.GET.get('title')
    message = request.GET.get('message')
    return render(request, 'error.html', {'title': title, 'message': message})

# Show Privacy Policy
def privacyPolicy(request):
    return render(request, 'privacy-policy.html')

# Show Terms of Use
def termsOfUse(request):
    return render(request, 'terms-of-use.html')