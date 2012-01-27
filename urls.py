from django.conf.urls.defaults import *
from django.shortcuts import redirect

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^account_tools/', include('account_tools.foo.urls')),
    (r'^/?$', lambda x: redirect("/~kedo/account_tools/change_password")),
    (r'^change_password/?$', 'chpass.views.change_password'),
    (r'^calnet/login/?$', 'calnet.views.login'),
    (r'^calnet/logout/?$', 'calnet.views.logout'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
