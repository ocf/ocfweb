import datetime
import socket

import ocflib.account.search as search
import ocflib.account.utils as account
import ocflib.misc.mail as mail
import ocflib.misc.validators as validators
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render

from ocfweb.atool.ocf.decorators import group_account_required
from ocfweb.atool.ocf.decorators import login_required
from ocfweb.atool.vhost.forms import VirtualHostForm


@login_required
@group_account_required
def request_vhost(request):
    user = request.session['ocf_user']
    attrs = search.user_attrs(user)
    error = None

    if account.has_vhost(user):
        return render(
            request,
            'already_have_vhost.html',
            {
                'user': user
            },
        )

    if request.method == 'POST':
        form = VirtualHostForm(request.POST)

        if form.is_valid():
            requested_subdomain = form.cleaned_data['requested_subdomain']
            requested_why = form.cleaned_data['requested_why']
            comments = form.cleaned_data['comments']
            your_name = form.cleaned_data['your_name']
            your_email = form.cleaned_data['your_email']
            your_position = form.cleaned_data['your_position']

            full_domain = '{}.berkeley.edu'.format(requested_subdomain)

            # verify that the requested domain is available
            if validators.host_exists(full_domain):
                error = 'The domain you requested is not available. ' + \
                    'Please select a different one.'

            if not validators.valid_email(your_email):
                error = "The email you entered doesn't appear to be " + \
                    'valid. Please double-check it.'

            if not error:
                # send email to hostmaster@ocf and redirect to success page
                ip_addr = get_client_ip(request)

                try:
                    ip_reverse = socket.gethostbyaddr(ip_addr)[0]
                except:
                    ip_reverse = 'unknown'

                subject = 'Virtual Hosting Request: {} ({})'.format(
                    full_domain, user)
                message = (
                    'Virtual Hosting Request:\n' +
                    '  - OCF Account: {user}\n' +
                    '  - OCF Account Title: {title}\n' +
                    '  - Requested Subdomain: {full_domain}\n' +
                    '  - Current URL: https://ocf.io/{user}/\n' +
                    '\n' +
                    'Request Reason:\n' +
                    '{requested_why}\n\n' +
                    'Comments/Special Requests:\n' +
                    '{comments}\n\n' +
                    'Requested by:\n' +
                    '  - Name: {your_name}\n' +
                    '  - Position: {your_position}\n' +
                    '  - Email: {your_email}\n' +
                    '  - IP Address: {ip_addr} ({ip_reverse})\n' +
                    '  - User Agent: {user_agent}\n' +
                    '\n\n' +
                    '--------\n' +
                    'Request submitted to atool ({hostname}) on {now}.\n' +
                    '{full_path}').format(
                        user=user,
                        title=attrs['cn'][0],
                        full_domain=full_domain,
                        requested_why=requested_why,
                        comments=comments,
                        your_name=your_name,
                        your_position=your_position,
                        your_email=your_email,
                        ip_addr=ip_addr,
                        ip_reverse=ip_reverse,
                        user_agent=request.META.get('HTTP_USER_AGENT'),
                        now=datetime.datetime.now().strftime(
                            '%A %B %e, %Y @ %I:%M:%S %p'),
                        hostname=socket.gethostname(),
                        full_path=request.build_absolute_uri())

                try:
                    mail.send_mail('hostmaster@ocf.berkeley.edu', subject, message, sender=your_email)
                    return redirect(reverse('request_vhost_success'))
                except Exception as ex:
                    print(ex)
                    print('Failed to send vhost request email!')
                    error = \
                        'We were unable to submit your virtual hosting ' + \
                        'request. Please try again or email us at ' + \
                        'hostmaster@ocf.berkeley.edu'
    else:
        form = VirtualHostForm(initial={'requested_subdomain': user})

    group_url = 'http://www.ocf.berkeley.edu/~{0}/'.format(user)

    return render(
        request,
        'request_vhost.html',
        {
            'form': form,
            'user': user,
            'attrs': attrs,
            'group_url': group_url,
            'error': error
        },
    )


def request_vhost_success(request):
    return render(
        request,
        'successfully_submitted_vhost.html',
        {},
    )


# http://stackoverflow.com/a/5976065/450164
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip
