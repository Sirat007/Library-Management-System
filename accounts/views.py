from django.shortcuts import render,redirect
from django.views.generic import FormView
from django.contrib.auth.views import LoginView
from .forms import RegistrationForm
from django.urls import reverse_lazy
from django.contrib.auth import login,logout
from django.contrib import messages
from books.models import Book
from transactions.models import Borrowing_Details
from accounts.models import UserLibraryAccount
from django.contrib.auth.decorators import login_required
from . import forms
from django.db.utils import IntegrityError


# Create your views here.

class UserRegistrationView(FormView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('profile')

    def form_valid(self,form):
        try:
            user = form.save()
            login(self.request, user)
            return super().form_valid(form)
        except IntegrityError:
            form.add_error('username', 'Username already exists.')
            return self.form_invalid(form)
    

class UserLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('home')
    
    def form_valid(self,form):
        messages.success(self.request,'Logged In Successfully')
        return super().form_valid(form)
    
    def form_invalid(self,form):
        messages.error(self.request,'Logged in Informations Incorrect')
        return super().form_invalid(form)
    
@login_required
def profile_view(request):
    user_account = UserLibraryAccount.objects.get(user=request.user)
    transactions = Borrowing_Details.objects.filter(user=user_account)
    return render(request, 'profile.html', {'transactions': transactions})
    


def UserLogout(request):
    logout(request)
    return redirect('home')
