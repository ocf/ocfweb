from django.conf import settings
from django.shortcuts import render
from ocflib.vhost.mail import get_connection
from ocflib.vhost.mail import vhosts_for_user

from ocfweb.auth import group_account_required
from ocfweb.auth import login_required
from ocfweb.component.session import logged_in_user


@login_required
@group_account_required
def vhost_mail(request):
    user = logged_in_user(request)
    vhosts = vhosts_for_user(user)

    with get_connection(
        user=settings.OCFMAIL_USER,
        password=settings.OCFMAIL_PASSWORD,
    ) as c:
        return render(
            request,
            'account/vhost_mail/index.html',
            {
                'title': 'Mail Virtual Hosting',

                'c': c,
                'vhosts': sorted(vhosts),
            },
        )
