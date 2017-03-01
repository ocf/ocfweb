from django.conf.urls import url

from ocfweb.api import api

urlpatterns = [
    url(r'sign\.json', api.sign_text, name='sign-json'),
]
