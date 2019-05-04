from collections import namedtuple
from datetime import datetime

import ocflib.misc.validators
from django import forms
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from jinja2 import Environment
from jinja2 import PackageLoader
from ocflib.misc.mail import send_mail

from ocfweb.auth import calnet_required
from ocfweb.component.forms import wrap_validator

JINJA_MAIL_ENV = Environment(loader=PackageLoader('ocfweb', ''))


class NewReservationRequest(
    namedtuple(
        'NewReservationRequest', [
            'real_name',
            'contact_email',
            'group',
            'reason',
            'date',
            'starttime',
            'endtime',
        ],
    ),
):
    __slots__ = ()

    def to_dict(self):
        return self._asdict()


class RequestForm(forms.Form):

    error_css_class = 'error'
    required_css_class = 'required'

    real_name = forms.CharField(
        label='Full Name',
        widget=forms.TextInput(attrs={'placeholder': 'Oski Bear'}),
        min_length=3,
    )

    contact_email = forms.EmailField(
        label='Contact email',
        validators=[wrap_validator(ocflib.misc.validators.valid_email)],
        widget=forms.EmailInput(attrs={'placeholder': 'oski@berkeley.edu'}),
    )

    verify_contact_email = forms.EmailField(
        label='Confirm contact email',
        validators=[wrap_validator(ocflib.misc.validators.valid_email)],
        widget=forms.EmailInput(attrs={'placeholder': 'oski@berkeley.edu'}),
    )

    group = forms.CharField(
        label='Group',
        widget=forms.TextInput(attrs={'placeholder': 'Open Computing Facility'}),
        min_length=3,
    )

    reason = forms.CharField(
        label='Reason for reservation',
        widget=forms.Textarea(attrs={'placeholder': ''}),
    )

    date = forms.DateField(
        label='Date of reservation (yyyy-mm-dd)',
        widget=forms.DateInput(attrs={'placeholder': datetime.now().strftime('%Y-%m-%d')}),
    )

    starttime = forms.TimeField(
        label='Starting time of reservation (24 hour, i.e. 20:00)',
    )

    endtime = forms.TimeField(
        label='Ending time of reservation (24 hour, i.e. 22:00)',
    )

    disclaimer_agreement = forms.BooleanField(
        label='I agree with the above statement.',
        error_messages={
            'required': 'You must agree to our policies.',
        },
    )

    def clean_verify_(self):
        email = self.cleaned_data.get('contact_email')
        verify_contact_email = self.cleaned_data.get('verify_contact_email')

        if email != verify_contact_email:
            raise forms.ValidationError("Your emails don't match.")
        return verify_contact_email


@calnet_required
def request_reservation(request):
    status = 'new_request'

    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            req = NewReservationRequest(
                real_name=form.cleaned_data['real_name'],
                contact_email=form.cleaned_data['contact_email'],
                group=form.cleaned_data['group'],
                reason=form.cleaned_data['reason'],
                date=form.cleaned_data['date'],
                starttime=form.cleaned_data['starttime'],
                endtime=form.cleaned_data['endtime'],
            )

            send_request_to_officers(req)
            send_request_confirmation(req)

            return redirect(reverse('request_reservation_success'))

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


def request_reservation_success(request):
    return render(request, 'lab_reservations/pending.html', {'title': 'Reservation request successful'})


def send_request_to_officers(request):
    body = JINJA_MAIL_ENV.get_template(
        'lab_reservations/mail_templates/officer_notification.jinja',
    ).render(request=request)
    send_mail(
        'bod@ocf.berkeley.edu',
        f'New Lab Reservation Request: {request.group}',
        body,
        sender=request.contact_email,
    )


def send_request_confirmation(request):
    body = JINJA_MAIL_ENV.get_template(
        'lab_reservations/mail_templates/user_notification.jinja',
    ).render(request=request)
    send_mail(request.contact_email, '[OCF] Your reservation request has been submitted!', body)
