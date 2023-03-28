from django.shortcuts import render
from .forms import SignUpForm

# Create your views here.
def registerUser(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
