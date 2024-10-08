from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].help_text = None
        
        if not user.is_superuser:
            self.fields['username'].disabled = True
            self.fields['email'].disabled = True
            self.fields['special_user'].disabled = True
            self.fields['is_author'].disabled = True
            
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'special_user', 'is_auther']
        

class SignupForm(UserCreationForm):
    phone_number = forms.CharField(max_length=11, label='Phone Number')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')