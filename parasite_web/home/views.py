from django.shortcuts import render, redirect

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
    return render(request, 'settings.html')