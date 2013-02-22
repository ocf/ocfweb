from django import forms
from approve.validators import validate_email_host_exists, \
    validate_username_not_reserved
from ocf.utils import clean_password
from ocf.validators.password import validate_crack_strength, \
    validate_printable_ascii
from ocf.validators.user import validate_unused_name, \
    validate_name_characters


class ApproveForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ApproveForm, self).__init__(*args, **kwargs)

    ocf_login_name = forms.CharField(label="OCF Login Name",
        validators=[validate_unused_name, validate_name_characters, \
                    validate_username_not_reserved],
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
    contact_email = forms.EmailField(label="Contact E-Mail",
            validators=[validate_email_host_exists])
    verify_contact_email = forms.EmailField(label="Confirm Contact E-Mail",
            validators=[validate_email_host_exists])
    forward_email = forms.BooleanField(required=False,
        label="Forward @ocf E-Mail to Contact E-Mail",
        initial=True)

    disclaimer_agreement = forms.BooleanField(
            label="You have read, understood, and agreed to our policies.",
            error_messages={
                "required": "You did not agree to our policies."
                })

    def clean_password(self):
        data = self.cleaned_data.get("password")
        return clean_password(data)

    def clean_verify_password(self):
        password = self.cleaned_data.get("password")
        verify_password = clean_password(self.cleaned_data.get("verify_password"))

        if password and verify_password:
            if password != verify_password:
                raise forms.ValidationError("Your passwords don't match.")
        return verify_password

    def clean_verify_contact_email(self):
        email = self.cleaned_data.get("contact_email")
        verify_contact_email = self.cleaned_data.get("verify_contact_email")

        if email and verify_contact_email:
            if email != verify_contact_email:
                raise forms.ValidationError("Your emails don't match.")
        return verify_contact_email

class GroupApproveForm(ApproveForm):
    def __init__(self, *args, **kwargs):
        super(ApproveForm, self).__init__(*args, **kwargs)
