from django import forms
from django.utils.safestring import mark_safe
from django.conf import settings
from recaptcha import captcha

class ReCaptchaWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        return mark_safe("%s" % captcha.displayhtml(settings.RECAPTCHA_PUBLIC_KEY, use_ssl=True))
    def value_from_datadict(self, data, files, name):
        return [data.get("recaptcha_challenge_field", None),
                data.get("recaptcha_response_field", None)]
