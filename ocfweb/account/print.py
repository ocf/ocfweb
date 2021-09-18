import base64
from email.message import EmailMessage
from email.utils import make_msgid
from email.utils import parseaddr
import mimetypes
import os.path
import uuid
from io import BytesIO
import subprocess

import qrcode
from django import forms
from django.forms import widgets
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from paramiko import AuthenticationException
from paramiko import SSHClient
from paramiko.hostkeys import HostKeyEntry

from ocfweb.component.forms import Form

import ocflib.misc.validators as validators
from ocflib.misc.mail import MAIL_FROM
from ocflib.misc.mail import SENDMAIL_PATH


PRINT_FOLDER = '.user_print'

EMAIL_BODY = '''
<html>
    <body>
        <p>
            Hi {username},
        </p>

        <p>
            Below you can find the QR code to start your print in the OCF computer lab.
            Show the QR code in front of the camera at the remote printing computer,
            and it will start printing your document.
        </p>
        <img src="cid:{image_cid}">
        <p>
            Thanks for flying OCF! <br>
            ~ OCF volunteer staff
        </p>
    </body>
</html>
'''


def send_qr_mail(username: str, qr_code: bytes) -> None:
    """Send the QR code needed to start the print in the lab to the user.

    Based on https://stackoverflow.com/a/49098251/9688107
    """

    msg = EmailMessage()
    msg['Subject'] = 'OCF Remote Printing QR Code'
    msg['From'] = MAIL_FROM
    msg['To'] = f'{username}@ocf.berkeley.edu'

    msg.set_content(
        'Sorry, we were unable to display your QR, please use the QR code on the website!.'
    )

    image_cid = make_msgid(domain='ocf.berkeley.edu')
    msg.add_alternative(EMAIL_BODY.format(username=username, image_cid=image_cid), subtype='html')
    msg.get_payload()[1].add_related(qr_code,
                                     maintype='image',
                                     subtype='png',
                                     cid=image_cid
                                     )
    # we send the message via sendmail because direct traffic to port 25
    # is firewalled off
    p = subprocess.Popen((SENDMAIL_PATH, '-t', '-oi'),
                         stdin=subprocess.PIPE)
    p.communicate(msg.as_string().encode('utf8'))


def print(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = PrintForm(
            request.POST,
            request.FILES,
            initial={
                'double_or_single': 'single',
            },
        )
        qr_b64 = b''
        double_or_single = 'single'
        error = ''
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            file = request.FILES['file']

            double_or_single = form.cleaned_data['double_or_single']

            ssh = SSHClient()

            host_keys = ssh.get_host_keys()
            entry = HostKeyEntry.from_line(
                'ssh.ocf.berkeley.edu ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAqMkHVVoMl8md25iky7e2Xe3ARaC4H1PbIpv5Y+xT4KOT17gGvFSmfjGyW9P8ZTyqxq560iWdyELIn7efaGPbkUo9retcnT6WLmuh9nRIYwb6w7BGEEvlblBmH27Fkgt7JQ6+1sr5teuABfIMg22WTQAeDQe1jg0XsPu36OjbC7HjA3BXsiNBpxKDolYIXWzOD+r9FxZLP0lawh8dl//O5FW4ha1IbHklq2i9Mgl79wAH3jxf66kQJTvLmalKnQ0Dbp2+vYGGhIjVFXlGSzKsHAVhuVD6TBXZbxWOYoXanS7CC43MrEtBYYnc6zMn/k/rH0V+WeRhuzTnr/OZGJbBBw==',  # noqa
            )
            assert entry is not None  # should never be none as we are passing a static string above
            host_keys.add(
                'ssh.ocf.berkeley.edu',
                'ssh-rsa',
                entry.key,
            )

            try:
                ssh.connect(
                    'ssh.ocf.berkeley.edu',
                    username=username,
                    password=password,
                )
            except AuthenticationException:
                error = 'Authentication failed. Did you type the wrong username or password?'

            if not error:
                sftp = ssh.open_sftp()
                try:
                    folder = sftp.stat(PRINT_FOLDER)
                    if folder.FLAG_PERMISSIONS != 0o700:
                        sftp.chmod(PRINT_FOLDER, 0o700)
                except FileNotFoundError:
                    sftp.mkdir(PRINT_FOLDER, 0o700)
                try:
                    rid = uuid.uuid4().hex
                    filename = f'{rid}-{file.name}'
                    with sftp.open(os.path.join(PRINT_FOLDER, filename), 'wb+') as dest:
                        for chunk in file.chunks():
                            dest.write(chunk)
                except OSError as e:
                    error = 'Failed to open file in user home directory, ' + \
                        f'please report this to help@ocf.berkeley.edu with the traceback\n{e}'
                else:
                    qr = qrcode.QRCode(
                        version=1,
                        box_size=10,
                        border=5,
                    )
                    qr.add_data(f'{username}:{filename}:{double_or_single}')
                    qr.make(fit=True)
                    img = qr.make_image(fill='black', back_color='white')
                    buff = BytesIO()
                    img.save(buff, format='PNG')
                    qr_data = buff.getvalue()
                    qr_b64 = b'data:image/png;base64,%b' % base64.b64encode(qr_data)
        send_qr_mail(
            username=username,
            qr_code=qr_data,
        )
        return render(
            request,
            'account/print/qr.html',
            {
                'title': 'QR Code',
                'qr_b64': qr_b64.decode('utf-8'),
                'error': error,
            },
        )
    else:
        form = PrintForm(
            initial={
                'double_or_single': 'single',
            },
        )

        return render(
            request,
            'account/print/index.html', {
                'title': 'Print remotely',
                'form': form,
            },
        )


class PrintForm(Form):
    username = forms.CharField(
        label='OCF username',
        min_length=3,
        max_length=16,
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Password',
        min_length=8,
        max_length=256,
    )

    file = forms.FileField()

    PRINT_CHOICES = (
        (
            'single',
            'single sided -- one page per piece of paper',
        ),
        (
            'double',
            'double sided -- two pages per piece of paper',
        ),
    )

    double_or_single = forms.ChoiceField(
        choices=PRINT_CHOICES,
        label='Print double or single sided',
        widget=widgets.RadioSelect,
    )
