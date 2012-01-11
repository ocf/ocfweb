from django import forms
from recaptcha.fields import ReCaptchaField
from chpass.validators import validate_password

class ChpassForm(forms.Form):
    
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password", validators=[validate_password])
    recaptcha = ReCaptchaField()
