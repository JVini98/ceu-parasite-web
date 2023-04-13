from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    # Someone trying to access directly through the URL
    if (request.GET.get('error')):
        message = request.GET.get('error')
        formatMessage = '<div class="alert alert-danger" role="alert">' + message + '</div>'
        return render(request, 'home.html', {'message': formatMessage})
    else: 
        return render(request, 'home.html')

def logout(request):
    del request.session['user']
    return redirect('/')