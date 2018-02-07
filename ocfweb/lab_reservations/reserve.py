from collections import namedtuple

import ocflib.misc.validators
from django import forms
from django.shortcuts import render
from jinja2 import Environment
from jinja2 import PackageLoader
from ocflib.account.search import user_attrs_ucb
from ocflib.misc.mail import send_mail

from ocfweb.auth import calnet_required
from ocfweb.component.forms import wrap_validator


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
    ],
)):
    """Request for reservation request.
    :param real_name:
    :param contact_email:
    :param student_group:
    :param reason:
    :param date:
    :param starttime:
    :param endtime:
    """

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
            'lab_reservations/lab_reservations/cant-find-in-ldap.html',
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
            )

            send_request_to_officers(req)
            send_request_confirmation(req)

            return render(
                request,
                'lab_reservations/pending.html',
            )

    else:
        form = RequestForm()

    return render(
        request,
        'lab_reservations/index.html',
        {
            'form': form,
            'status': status,
            'title': 'Request the OCF Lab Space',
        },
    )


def reservation_requested(request):
    return render(request, 'lab_reservations/pending.html', {'title': 'Reservation request successful'})


def send_request_to_officers(request):
    body = JINJA_MAIL_ENV.get_template(
        'lab_reservations/mail_templates/officer_notification.jinja',
    ).render(request=request)
    send_mail('bod@ocf.berkeley.edu', 'New Lab Reservation Request', body)


def send_request_confirmation(request):
    body = JINJA_MAIL_ENV.get_template(
        'lab_reservations/mail_templates/user_notification.jinja',
    ).render(request=request)
    send_mail(request.contact_email, '[OCF] Your recent reservation request has been submitted!', body)
