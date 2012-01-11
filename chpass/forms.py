from django import forms
from recaptcha.fields import ReCaptchaField
from chpass.validators import validate_password

class ChpassForm(forms.Form):
    def __init__(self, ocf_accounts, *args, **kwargs):
        super(ChpassForm, self).__init__(*args, **kwargs)

        self.fields["ocf_account"] = forms.ChoiceField(choices=[(x,x) for x in ocf_accounts], label="OCF Account")
        self.fields.keyOrder = [
            "ocf_account",
            "new_password",
            "recaptcha"
        ]
    
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password", validators=[validate_password])
    recaptcha = ReCaptchaField(label="ReCaptcha")
