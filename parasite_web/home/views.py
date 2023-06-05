from django.shortcuts import render, redirect
from users.models import User
from .forms import NameForm

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

def account_settings(request):
    user = User.objects.get(email=request.session["user"])
    form = NameForm(initial={'first_name': user.first_name, 'last_name': user.last_name})
    if (request.GET.get('message')):
        message = request.GET.get('message')
        formatMessage = '<div class="alert alert-success" role="alert">' + message + '</div>'
        context = {"form": form, 'message': formatMessage}
    else: 
        context = {"form": form}
    return render(request, 'settings.html', context)

def update_user_name(request):
    if request.method == "POST":
        user = User.objects.get(email=request.session["user"])
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        message = 'Account settings updated successfully'
        return redirect(f'/account_settings?message={message}')