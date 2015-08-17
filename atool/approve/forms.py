import ocflib.account.validators as validators
import ocflib.misc.validators
from django import forms

from atool.utils import wrap_validator


class ApproveForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ApproveForm, self).__init__(*args, **kwargs)

    ocf_login_name = forms.CharField(
        label='OCF Login Name',
        validators=[wrap_validator(validators.validate_username)],
        min_length=3,
        max_length=8)

    # password is validated in clean since we need the username as part of the
    # password validation (to compare similarity)
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='New Password',
        min_length=8,
        max_length=64)

    verify_password = forms.CharField(
        widget=forms.PasswordInput,
        label='Confirm Password',
        min_length=8,
        max_length=64)
    contact_email = forms.EmailField(
        label='Contact E-Mail',
        validators=[wrap_validator(ocflib.misc.validators.valid_email)])

    verify_contact_email = forms.EmailField(label='Confirm Contact E-Mail')

    disclaimer_agreement = forms.BooleanField(
        label='You have read, understood, and agreed to our policies.',
        error_messages={
            'required': 'You did not agree to our policies.'
        })

    def clean_verify_password(self):
        password = self.cleaned_data.get('password')
        verify_password = self.cleaned_data.get('verify_password')

        if password and verify_password:
            if password != verify_password:
                raise forms.ValidationError("Your passwords don't match.")
        return verify_password

    def clean_verify_contact_email(self):
        email = self.cleaned_data.get('contact_email')
        verify_contact_email = self.cleaned_data.get('verify_contact_email')

        if email and verify_contact_email:
            if email != verify_contact_email:
                raise forms.ValidationError("Your emails don't match.")
        return verify_contact_email

    def clean(self):
        cleaned_data = super(ApproveForm, self).clean()

        # validate password (requires username to check similarity)
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            wrap_validator(validators.validate_password)(username, password)
