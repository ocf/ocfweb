from django import forms
from recaptcha.fields import ReCaptchaField
from django.conf import settings
from ocf.validators.password import validate_crack_strength, validate_printable_ascii
from ocf import utils


class ChpassForm(forms.Form):
    def __init__(self, ocf_accounts, calnet_uid, *args, **kwargs):
        super(ChpassForm, self).__init__(*args, **kwargs)
        self.calnet_uid = calnet_uid
        self.fields["ocf_account"] = forms.ChoiceField(choices=[
            (x, x) for x in ocf_accounts],
            label="OCF Account")
        self.fields.keyOrder = [
            "ocf_account",
            "new_password",
            "confirm_password",
            "recaptcha"
        ]

    new_password = forms.CharField(widget=forms.PasswordInput,
        label="New Password",
        validators=[validate_crack_strength, validate_printable_ascii],
        min_length=8,
        max_length=64)
    confirm_password = forms.CharField(widget=forms.PasswordInput,
        label="Confirm Password",
        min_length=8,
        max_length=64)
    recaptcha = ReCaptchaField(label="ReCaptcha")

    def clean_ocf_account(self):
        data = self.cleaned_data["ocf_account"]
        data = utils.clean_user_account(data)
        if not utils.user_exists(data):
            raise forms.ValidationError("OCF user account does not exist.")

        ocf_accounts = utils.users_by_calnet_uid(self.calnet_uid)
        if self.calnet_uid in settings.TESTER_CALNET_UIDS:
            ocf_accounts.extend(settings.TEST_OCF_ACCOUNTS)

        if data not in ocf_accounts:
            raise forms.ValidationError("OCF user account and CalNet UID mismatch.")

        return data

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
