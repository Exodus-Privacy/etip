from account.forms.registration import CustomUserCreationForm
from django.shortcuts import render


# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            errors = form.errors
            return render(request, 'account/register.html', {'errors': errors})

    return render(request, 'account/register.html')
