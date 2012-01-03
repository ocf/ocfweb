from django import forms
from django.conf import settings
from django.utils.encoding import smart_unicode
from recaptcha import captcha
from recaptcha.widgets import ReCaptchaWidget
import sys

class ReCaptchaField(forms.CharField):
    default_error_messages = {
        "captcha_invalid": "Invalid captcha"
    }

    def __init__(self, *args, **kwargs):
        super(ReCaptchaField, self).__init__(*args, **kwargs)
        self.widget = ReCaptchaWidget
        self.required = True
        super(ReCaptchaField, self).__init__(*args, **kwargs)

    def get_remote_ip(self):
    	f = sys._getframe()
    	while f:
    	    if "request" in f.f_locals:
    	    	request = f.f_locals["request"]
    	    	if request:
    	    	    return request.META["REMOTE_ADDR"]
    	    f = f.f_back
    	return None

    def clean(self, values):
        super(ReCaptchaField, self).clean(values[1])
        recaptcha_challenge_value = smart_unicode(values[0])
        recaptcha_response_value = smart_unicode(values[1])
        check_captcha = captcha.submit(recaptcha_challenge_value,
                recaptcha_response_value, settings.RECAPTCHA_PRIVATE_KEY,
                self.get_remote_ip())
        if not check_captcha.is_valid:
            raise forms.util.ValidationError(self.error_messages['captcha_invalid'])
        return values[0]
