import email.mime.text
import subprocess
from collections import namedtuple
from email.utils import parseaddr

import ocflib.misc.validators
from django import forms
from django.shortcuts import render
from jinja2 import Environment
from jinja2 import PackageLoader
from ocflib.account.search import user_attrs_ucb

from ocfweb.auth import calnet_required
from ocfweb.component.forms import wrap_validator

SENDMAIL_PATH = '/usr/sbin/sendmail'
MAIL_FROM = 'Open Computing Facility <help@ocf.berkeley.edu>'

JINJA_MAIL_ENV = Environment(loader=PackageLoader('ocfweb', ''))


class NewReservationRequest(namedtuple(
    'NewReservationRequest', [
        'real_name',
        'contact_email',
        'student_group',
        'reason',
        'date',
        'starttime',
        'endtime',
        'handle_warnings',
    ],
)):
    """Request for account creation.
    :param real_name:
    :param contact_email:
    :param student_group:
    :param reason:
    :param date:
    :param starttime:
    :param endtime:
    :param handle_warnings: one of WARNINGS_WARN, WARNINGS_SUBMIT
        WARNINGS_WARN: don't create request, return warnings
        WARNINGS_SUBMIT: submit for staff approval
    """
    WARNINGS_WARN = 'warn'
    WARNINGS_SUBMIT = 'submit'

    def to_dict(self):
        return {
            field: getattr(self, field)
            for field in self._fields
        }


class RequestForm(forms.Form):

    error_css_class = 'error'
    required_css_class = 'required'

    real_name = forms.CharField(
        label='Full Name',
        widget=forms.TextInput(attrs={'placeholder': 'Jane Doe'}),
        min_length=3,
        max_length=32,
    )

    contact_email = forms.EmailField(
        label='Contact e-mail',
        validators=[wrap_validator(ocflib.misc.validators.valid_email)],
        widget=forms.EmailInput(attrs={'placeholder': 'janedoe@berkeley.edu'}),
    )

    verify_contact_email = forms.EmailField(
        label='Confirm contact e-mail',
        widget=forms.EmailInput(attrs={'placeholder': 'janedoe@berkeley.edu'}),
    )

    student_group = forms.CharField(
        label='Student Group',
        widget=forms.TextInput(attrs={'placeholder': 'OCF'}),
        min_length=3,
        max_length=32,
    )

    reason = forms.CharField(
        label='Reason for reservation',
        widget=forms.TextInput(attrs={'placeholder': ''}),
    )

    date = forms.DateField(
        label='Date of reservation (mm/dd/yy)',
        widget=forms.DateInput(attrs={'placeholder': '02/28/18'}),
    )

    starttime = forms.TimeField(
        label='Starting time of reservation (xx:xx)',
    )

    endtime = forms.TimeField(
        label='Ending time of reservation (xx:xx)',
    )

    disclaimer_agreement = forms.BooleanField(
        label='I agree with the above statement.',
        error_messages={
            'required': 'You must agree to our policies.',
        },
    )

    def clean_verify_contact_email(self):
        email = self.cleaned_data.get('contact_email')
        verify_contact_email = self.cleaned_data.get('verify_contact_email')

        if email and verify_contact_email:
            if email != verify_contact_email:
                raise forms.ValidationError("Your emails don't match.")
        return verify_contact_email


@calnet_required
def request_reservation(request):
    calnet_uid = request.session['calnet_uid']
    status = 'new_request'

    # ensure we can even find them in university LDAP
    # (alumni etc. might not be readable in LDAP but can still auth via CalNet)
    if not user_attrs_ucb(calnet_uid):
        return render(
            request,
            'reservations/reservations/cant-find-in-ldap.html',
            {
                'calnet_uid': calnet_uid,
                'title': 'Unable to read account information',
            },
        )

    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            req = NewReservationRequest(
                real_name=form.cleaned_data['real_name'],
                contact_email=form.cleaned_data['contact_email'],
                student_group=form.cleaned_data['student_group'],
                reason=form.cleaned_data['reason'],
                date=form.cleaned_data['date'],
                starttime=form.cleaned_data['starttime'],
                endtime=form.cleaned_data['endtime'],
                handle_warnings=NewReservationRequest.WARNINGS_WARN,
            )

            send_request_to_officers(req)
            send_request_confirmation(req)

            return render(
                request,
                'reservations/pending.html',
            )

    else:
        form = RequestForm()

    return render(
        request,
        'reservations/index.html',
        {
            'form': form,
            'status': status,
            'title': 'Request the OCF Lab Space',
        },
    )


def reservation_requested(request):
    return render(request, 'reservations/pending.html', {'title': 'Account request successful'})


def send_mail(to, subject, body, sender=MAIL_FROM):
    """Send a plain-text mail message.
    `body` should be a string with newlines, wrapped at about 80 characters."""

    if not ocflib.misc.validators.valid_email(parseaddr(sender)[1]):
        raise ValueError('Invalid sender address.')

    if not ocflib.misc.validators.valid_email(parseaddr(to)[1]):
        raise ValueError('Invalid recipient address.')

    msg = email.mime.text.MIMEText(body)

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to

    # we send the message via sendmail, since we may one day prohibit traffic
    # to port 25 that doesn't go via the system mailserver
    p = subprocess.Popen(
        (SENDMAIL_PATH, '-t', '-oi'),
        stdin=subprocess.PIPE,
    )
    p.communicate(msg.as_string().encode('utf8'))


def send_request_to_officers(request):
    body = JINJA_MAIL_ENV.get_template(
        'reservations/mail_templates/officer_notification.jinja',
    ).render(request=request)
    send_mail('welty025@berkeley.edu', 'New Lab Reservation Request', body)


def send_request_confirmation(request):
    body = JINJA_MAIL_ENV.get_template(
        'reservations/mail_templates/user_notification.jinja',
    ).render(request=request)
    send_mail(request.contact_email, '[OCF] Your recent reservation request has been submitted!', body)
