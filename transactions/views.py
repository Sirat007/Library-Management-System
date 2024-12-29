from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import DepositForm
from accounts.models import UserLibraryAccount
from .models import Deposit,Borrowing_Details
from django.urls import reverse_lazy
from django.utils import timezone
from books.models import Book
from django.contrib import messages

# Create your views here.

@login_required
def borrow_book(request,pk):
    book = get_object_or_404(Book, pk=pk)
    user_account = request.user.account

    if user_account.balance >= book.borrowing_price:
        Borrowing_Details.objects.create(
            user=user_account,
            book=book,
            amount=book.borrowing_price
        )

        user_account.balance -= book.borrowing_price
        user_account.save()
        messages.success(request, f"You  borrowed this {book.title}.")
        return redirect('profile')
    else:
        messages.error(request,f'Your balance  {user_account.balance} is Insufficient')

    return render(request,'details.html',{'book':book})



@login_required
def deposit_money(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user_account = request.user.account

            Deposit.objects.create(
                user = user_account,
                amount = amount
            )
            user_account.balance += amount
            user_account.save()
            return redirect('profile')
    else:
        form = DepositForm()

    return render(request,'deposit.html',{'form':form})

@login_required
def return_book(request,transaction_id):
    transaction = get_object_or_404(Borrowing_Details,id=transaction_id)
    user_account = request.user.account

    if request.method =='POST':
        if not transaction.return_date:
            transaction.return_date = timezone.now()
            transaction.save()

            user_account.balance += transaction.amount
            user_account.save()

            return redirect('profile')
    
    return render(request,'return_book.html',{'transaction': transaction})