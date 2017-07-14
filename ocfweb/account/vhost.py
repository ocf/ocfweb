import datetime
import re
import socket
from textwrap import dedent

from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.safestring import mark_safe
from ipware.ip import get_real_ip
from ocflib.account.search import user_attrs
from ocflib.misc.mail import send_mail
from ocflib.misc.validators import host_exists
from ocflib.misc.validators import valid_email
from ocflib.misc.whoami import current_user_formatted_email
from ocflib.vhost.web import eligible_for_vhost
from ocflib.vhost.web import has_vhost

from ocfweb.auth import login_required
from ocfweb.component.forms import Form
from ocfweb.component.session import logged_in_user


def valid_domain(domain):
    if not re.match(r'^[a-zA-Z0-9]+\.berkeley\.edu$', domain):
        return False
    return not host_exists(domain)


def valid_domain_external(domain):
    return bool(re.match(r'([a-zA-Z0-9]+\.)+[a-zA-Z0-9]{2,}', domain))


@login_required
def request_vhost(request):
    user = logged_in_user(request)
    attrs = user_attrs(user)
    is_group = 'callinkOid' in attrs
    error = None

    if has_vhost(user):
        return render(
            request,
            'account/vhost/already_have_vhost.html',
            {
                'title': 'You already have virtual hosting',
                'user': user,
            },
        )
    elif not eligible_for_vhost(user):
        return render(
            request,
            'account/vhost/not_eligible.html',
            {
                'title': 'You are not eligible for virtual hosting',
                'user': user,
            },
        )

    if request.method == 'POST':
        form = VirtualHostForm(is_group, request.POST)

        if form.is_valid():
            requested_subdomain = form.cleaned_data['requested_subdomain']
            requested_why = form.cleaned_data['requested_why']
            comments = form.cleaned_data['comments']
            your_name = form.cleaned_data['your_name'] if is_group else attrs['cn'][0]
            your_email = form.cleaned_data['your_email']
            your_position = form.cleaned_data['your_position']

            if not error:
                # send email to hostmaster@ocf and redirect to success page
                ip_addr = get_real_ip(request)

                try:
                    ip_reverse = socket.gethostbyaddr(ip_addr)[0]
                except:
                    ip_reverse = 'unknown'

                subject = 'Virtual Hosting Request: {} ({})'.format(
                    requested_subdomain,
                    user,
                )
                message = dedent('''\
                    Virtual Hosting Request:
                      - OCF Account: {user}
                      - OCF Account Title: {title}
                      - Requested Subdomain: {requested_subdomain}
                      - Current URL: https://www.ocf.berkeley.edu/~{user}/

                    Request Reason:
                    {requested_why}

                    Comments/Special Requests:
                    {comments}

                    Requested by:
                      - Name: {your_name}
                      - Position: {your_position}
                      - Email: {your_email}
                      - IP Address: {ip_addr} ({ip_reverse})
                      - User Agent: {user_agent}

                    --------
                    Request submitted to ocfweb ({hostname}) on {now}.
                    {full_path}''').format(
                    user=user,
                    title=attrs['cn'][0],
                    requested_subdomain=requested_subdomain,
                    requested_why=requested_why,
                    comments=comments,
                    your_name=your_name,
                    your_position=your_position,
                    your_email=your_email,
                    ip_addr=ip_addr,
                    ip_reverse=ip_reverse,
                    user_agent=request.META.get('HTTP_USER_AGENT'),
                    now=datetime.datetime.now().strftime(
                        '%A %B %e, %Y @ %I:%M:%S %p',
                    ),
                    hostname=socket.gethostname(),
                    full_path=request.build_absolute_uri(),
                )

                try:
                    send_mail(
                        'hostmaster@ocf.berkeley.edu' if not settings.DEBUG else current_user_formatted_email(),
                        subject,
                        message,
                        sender=your_email,
                    )
                except Exception as ex:
                    # TODO: report via ocflib
                    print(ex)
                    print('Failed to send vhost request email!')
                    error = \
                        'We were unable to submit your virtual hosting ' + \
                        'request. Please try again or email us at ' + \
                        'hostmaster@ocf.berkeley.edu'
                else:
                    return redirect(reverse('request_vhost_success'))
    else:
        form = VirtualHostForm(is_group, initial={'requested_subdomain': user + '.berkeley.edu'})

    group_url = 'https://www.ocf.berkeley.edu/~{}/'.format(user)

    return render(
        request,
        'account/vhost/index.html',
        {
            'attrs': attrs,
            'error': error,
            'form': form,
            'group_url': group_url,
            'is_group': is_group,
            'title': 'Request virtual hosting',
            'user': user,
        },
    )


def request_vhost_success(request):
    return render(
        request,
        'account/vhost/success.html',
        {
            'title': 'Virtual host successfully submitted',
        },
    )


class VirtualHostForm(Form):
    # requested subdomain
    requested_own_domain = forms.ChoiceField(
        choices=[
            (
                False, 'I would like to request a berkeley.edu domain \
                     (most student groups want this).',
            ),
            (True, 'I want to use the domain I already own.'),
        ],
        widget=forms.RadioSelect(),
    )

    requested_subdomain = forms.CharField(
        label='Requested domain:',
        min_length=1,
        max_length=32,
        widget=forms.TextInput(attrs={'placeholder': 'mysite.berkeley.edu'}),
    )

    requested_why = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 60, 'rows': 3}),
        label='Please explain why you would like to use the requested \
               domain instead of your current address on \
               ocf.berkeley.edu.',
        min_length=1,
        max_length=1024,
    )

    # website requirements
    website_complete = forms.BooleanField(
        label='The website is already complete and uploaded to the OCF \
               server. It is not just a placeholder.')

    website_hosted_by_ocf = forms.BooleanField(
        label="The website is substantially hosted by the OCF. It \
               doesn't use frames, redirects, proxies, or other tricks to \
               circumvent this policy.")

    # see __init__ method below for the labels on these
    website_ocf_banner = forms.BooleanField()

    website_disclaimer_text = forms.BooleanField()

    website_updated_software = forms.BooleanField(
        label='Any software (such as WordPress, Joomla, Drupal, etc.) \
               is fully updated, and the maintainer will update it \
               regularly to ensure the site is not compromised. (If \
               you are not using any software on your website, check \
               this box and move on.)')

    your_email = forms.EmailField(
        label='Your email address:',
        min_length=1,
        max_length=64,
    )

    # also see __init__
    your_position = forms.CharField(
        min_length=1,
        max_length=64,
    )

    comments = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 60, 'rows': 3}),
        label='Please write any special requests and/or comments you have:',
        required=False,
        min_length=1,
        max_length=1024,
    )

    def __init__(self, is_group=True, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)

        # It's pretty derpy that we have to set the labels here, but we can't
        # use `reverse` during import time since URLs aren't configured yet
        # (this module gets imported as part of the URL configuration).
        #
        # Normally using `reverse_lazy` would fix that, but we can't use that
        # either because `mark_safe` isn't lazy.
        self.fields['website_disclaimer_text'].label = mark_safe((
            'If we are a student group, we have placed the <a href="{}">university-mandated '
            'disclaimer</a> on each page of our site.'
        ).format(reverse('doc', args=('services/vhost',))))

        self.fields['website_ocf_banner'].label = mark_safe((
            'There is a <a href="{}">Hosted by the OCF</a> banner image '
            'visible on the home page.'
        ).format(reverse('doc', args=('services/vhost/badges',))))

        # These just require some runtime info
        self.fields['your_position'].label = mark_safe(
            'Your position in group:' if is_group else 'Your academic post:',
        )

        self.fields['your_position'].widget = forms.TextInput(
            attrs={'placeholder': 'Webmaster' if is_group else 'E.g., Professor of Math'},
        )

        if is_group:
            self.fields['your_name'] = forms.CharField(
                label='Your full name:',
                min_length=1,
                max_length=64,
            )

    def clean_requested_subdomain(self):
        requested_subdomain = self.cleaned_data['requested_subdomain'].lower().strip()

        if self.cleaned_data['requested_own_domain']:
            if not valid_domain_external(requested_subdomain):
                raise forms.ValidationError(
                    'This does not appear to be a valid domain. '
                    'Please check your response and try again.',
                )
            return requested_subdomain

        if not requested_subdomain.endswith('.berkeley.edu'):
            raise forms.ValidationError(
                'The domain you entered does not end in ".berkeley.edu". '
                'Maybe add ".berkeley.edu" to the end?',
            )

        if not valid_domain(requested_subdomain):
            raise forms.ValidationError(
                'The domain you requested is not available. '
                'Please select a different one.',
            )

        return requested_subdomain

    def clean_your_email(self):
        your_email = self.cleaned_data['your_email']
        if not valid_email(your_email):
            raise forms.ValidationError(
                "The email you entered doesn't appear to be "
                'valid. Please double-check it.',
            )
        return your_email
