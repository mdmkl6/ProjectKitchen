from django import forms 

class ToBuyForm(forms.Form):
    text = forms.CharField(max_length=40, 
        widget=forms.TextInput(
            attrs={'class' : 'form-control', 'placeholder' : 'Enter product', 'aria-label' : 'ToBuy', 'aria-describedby' : 'add-btn'}))