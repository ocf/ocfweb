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
    password = forms.CharField(widget=forms.PasswordInput,
        label="New Password",
        validators=[validate_crack_strength, validate_printable_ascii],
        min_length=8,
        max_length=64)
    verify_password = forms.CharField(widget=forms.PasswordInput,
        label="Confirm Password",
        min_length=8,
        max_length=64)
    contact_email = forms.EmailField(label="Content E-Mail")
    forward_email = forms.BooleanField(label="Forward @ocf E-Mail to Contact E-Mail",
        required=False,
        initial=True)

    disclaimer_agreement = forms.BooleanField(label="You have read, understood, and agreed to our policies.")

    def clean_password(self):
        data = self.cleaned_data.get("password")
        return utils.clean_password(data)

    def clean_verify_password(self):
        password = self.cleaned_data.get("password")
        verify_password = utils.clean_password(self.cleaned_data.get("verify_password"))

        if password and verify_password:
            if password != verify_password:
                raise forms.ValidationError("Your passwords don't match.")
        return verify_password
