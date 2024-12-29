from django import forms 
from .models import Deposit,Borrowing_Details

class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrowing_Details
        fields = ['book']

        

class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ['amount']

    def clean_amount(self):
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount')
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount}$'
            )
        
        return amount