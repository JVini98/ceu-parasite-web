from django.shortcuts import render, HttpResponse
from .forms import UserForm
from .models import User

# Create your views here.
def loginUser(request): 
    return render(request, 'login.html')

def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = User(first_name = form.cleaned_data.get("first_name"),
                        last_name = form.cleaned_data.get("last_name"),
                        email = form.cleaned_data.get("email"),
                        password = form.cleaned_data.get("password1")
                        )
            user.save()
            return render(request, 'login.html', {'form': form})
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})

