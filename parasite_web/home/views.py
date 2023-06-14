from django.shortcuts import render, redirect
from users.models import User
from .forms import NameForm, PasswordFormStyle
from django.contrib.auth.hashers import make_password

# Create your views here.
def home(request):
    # Restricted accessing through the URL
    if (request.GET.get('error')):
        message = request.GET.get('error')
        formatMessage = '<div class="alert alert-danger" role="alert">' + message + '</div>'
        return render(request, 'home.html', {'message': formatMessage})
    # Display message when the user is logged in
    elif ('user' in request.session): 
        message = "Welcome back, <b>" + request.session['user'] + "</b>! We are glad to see you again." 
        formatMessage = '<div class="alert alert-success alert-dismissible fade show" role="alert">' + message + '</div>'
        return render(request, 'home.html', {'message': formatMessage})
    else: 
        return render(request, 'home.html')

def logout(request):
    del request.session['user']
    return redirect('/')

# Show user information
def account_settings(request):
    # Check if the user is logged in
    if ('user' in request.session):
        user = User.objects.get(email=request.session["user"])
        form_name = NameForm(initial={'first_name': user.first_name, 'last_name': user.last_name})
        form_password = PasswordFormStyle()
        if (request.GET.get('message')):
            message = request.GET.get('message')
            formatMessage = '<div class="alert alert-success" role="alert">' + message + '</div>'
            context = {"form_name": form_name, "form_password": form_password,'message': formatMessage}
        elif (request.GET.get('error')):
            error = request.GET.get('error')
            formatMessage = '<div class="alert alert-danger" role="alert">' + error + '</div>'
            context = {"form_name": form_name, "form_password": form_password,'message': formatMessage}
        else: 
            context = {"form_name": form_name, "form_password": form_password}
        return render(request, 'settings.html', context)
    # The user is not logged in
    else: 
        error = 'To access the account settings section, you need to login'
        return redirect(f'/?error={error}')

# Change the user information
def update_user_name(request):
    if request.method == "POST":
        user = User.objects.get(email=request.session["user"])
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        message = 'Account settings updated successfully'
        return redirect(f'/account_settings?message={message}')

# Change a user password
def update_password(request):
    if request.method == 'POST':
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        # Check if passwords match
        if (pass1 == pass2):
            user = User.objects.get(email=request.session["user"])
            user.password = make_password(pass1)
            user.save()
            message = "Your password was successfully changed"
            return redirect(f'/account_settings?message={message}')
        # Password do not match
        else: 
            error = "The passwords do not match. Plase make sure you typed them correctly."
            return redirect(f'/account_settings?error={error}')

# Delete the current user
def delete_user(request):
    if request.method == 'POST':
        user = User.objects.get(email=request.session["user"])
        try: 
            user.delete()
            message = "Your user was successfully deleted"
            return redirect(f'/logout')
        except Exception as exception:
            return redirect(f'/account_settings?message={str(exception)}')

# Show Cookies
def cookies(request):
    return render(request, 'cookies.html')