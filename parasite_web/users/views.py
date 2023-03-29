from django.shortcuts import render, HttpResponse
from .forms import SignUpForm

# Create your views here.
def loginUser(request): 
    return render(request, 'login.html')

def registerUser(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            print("Todo ha ido bien")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

