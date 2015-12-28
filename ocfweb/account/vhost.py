import datetime
import re
import socket

from django import forms
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.safestring import mark_safe
from ocflib.account.search import user_attrs
from ocflib.account.utils import has_vhost
from ocflib.misc.mail import send_mail
from ocflib.misc.validators import host_exists
from ocflib.misc.validators import valid_email

from ocfweb.auth import group_account_required
from ocfweb.auth import login_required


def valid_domain(domain):
    if not re.match('^[a-zA-Z]+\.berkeley\.edu$', domain):
        return False
    if domain.count('.') != 2:
        return False
    return not host_exists(domain)


@login_required
@group_account_required
def request_vhost(request):
    user = request.session['ocf_user']
    attrs = user_attrs(user)
    error = None

    if has_vhost(user):
        return render(
            request,
            'vhost/already_have_vhost.html',
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
            if not valid_domain(full_domain):
                error = 'The domain you requested is not available. ' + \
                    'Please select a different one.'

            if not valid_email(your_email):
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
                    'Request submitted to ocfweb ({hostname}) on {now}.\n' +
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
                    send_mail('hostmaster@ocf.berkeley.edu', subject, message, sender=your_email)
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
        'vhost/index.html',
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
        'vhost/success.html',
        {},
    )


# TODO: use ipware which we already dep
# http://stackoverflow.com/a/5976065/450164
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


class VirtualHostForm(forms.Form):
    # requested subdomain
    requested_subdomain = forms.CharField(
        label='Requested domain:',
        min_length=1,
        max_length=32)

    requested_why = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 60, 'rows': 3}),
        label='Please explain why you would like to use the requested \
               domain instead of your current address on \
               ocf.berkeley.edu.',
        min_length=1,
        max_length=1024)

    # web site requirements
    website_complete = forms.BooleanField(
        label='Our site is already complete and uploaded to the OCF \
               server. The website is not just a placeholder.')

    website_hosted_by_ocf = forms.BooleanField(
        label="Our site is substantially hosted by the OCF. We \
               don't use frames, redirects, proxies, or other tricks to \
               circumvent this policy.")

    website_ocf_banner = forms.BooleanField(
        label=mark_safe("We have placed a \
                <a href=\"http://www.ocf.berkeley.edu/images/hosted-logos/\">\
                Hosted by the OCF</a> banner image on our site."))

    website_disclaimer_text = forms.BooleanField(
        label=mark_safe("We have placed the \
               <a href=\"http://ocf.io/vhost#disclaimer\">\
               university-required disclaimer</a> on each page of our site."))

    website_updated_software = forms.BooleanField(
        label='Any software (such as WordPress, Joomla, Drupal, etc.) \
               is fully updated, and we will commit to updating it \
               regularly to ensure our site is not compromised. (If \
               you are not using any software on your website, check \
               this box and move on.)')

    # confirm request
    your_name = forms.CharField(
        label='Your full name:',
        min_length=1,
        max_length=64)

    your_email = forms.EmailField(
        label='Your email address:',
        min_length=1,
        max_length=64)

    your_position = forms.CharField(
        label='Your position in group:',
        min_length=1,
        max_length=64)

    comments = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 60, 'rows': 3}),
        label='Please write any special requests and/or comments you have:',
        required=False,
        min_length=1,
        max_length=1024)
