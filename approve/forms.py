from django import forms
from ocf.validators.password import validate_crack_strength, validate_printable_ascii
from ocf.validators.user import validate_unused_name

class ApproveForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ApproveForm, self).__init__(*args, **kwargs)

    ocf_login_name = forms.CharField(label="OCF Login Name",
        validators=[validate_unused_name],
        min_length=3,
        max_length=8)
    new_password = forms.CharField(widget=forms.PasswordInput,
        label="New Password",
        validators=[validate_crack_strength, validate_printable_ascii],
        min_length=8,
        max_length=64)
    confirm_password = forms.CharField(widget=forms.PasswordInput,
        label="Confirm Password",
        min_length=8,
        max_length=64)
    contact_email = forms.EmailField(label="Content E-Mail")
    forward_email = forms.BooleanField(label="Forward @ocf E-Mail to Contact E-Mail",
        required=False,
        initial=True)

    disclaimer_agreement = forms.BooleanField(label="You have read, understood, and agreed to our policies.")

    def clean_new_password(self):
        data = self.cleaned_data.get("new_password")
        return utils.clean_password(data)

    def clean_confirm_password(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_password = utils.clean_password(self.cleaned_data.get("confirm_password"))

        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError("Your passwords don't match.")
        return confirm_password
