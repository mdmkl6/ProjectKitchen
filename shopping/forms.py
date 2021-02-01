from django import forms 


class ToBuyForm(forms.Form):
    text = forms.CharField(max_length=40, 
        widget=forms.TextInput(
            attrs={'class' : 'form-control form-autocomplete', 'placeholder' : 'Enter product', 'aria-label' : 'ToBuy', 'aria-describedby' : 'add-btn'}))
    amount = forms.CharField(max_length=40, 
        widget=forms.TextInput(
            attrs={'class' : 'form-control', 'placeholder' : 'Enter amount', 'aria-label' : 'ToBuy', 'aria-describedby' : 'add-btn'}))
