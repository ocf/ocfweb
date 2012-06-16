from django import forms
from django.forms import widgets

class CommandForm(forms.Form):

    username = forms.CharField(label="OCF Username",
        min_length=3,
        max_length=8)
    password = forms.CharField(widget=forms.PasswordInput,
        label="Password",
        min_length=8,
        max_length=64)

    COMMAND_CHOICES = (
        ("/opt/ocf/bin/paper", "paper quota — how many pages you have printed this semester"),
        ("/usr/bin/quota -svQ", "disk quota — how much disk space you have used and how much you have left"),
        ("/opt/ocf/bin/spam-setup", "spam-setup — set up SpamAssassin spam filtering for your OCF email"),
        ("/opt/ocf/bin/makehttp", "makehttp — set up the web space for your OCF account"),
        ("echo yes | /opt/ocf/bin/makemysql", "makemysql — reset your MySQL database password, or create a new MySQL database (copy down the password somewhere SECURE)"),
    )

    command_to_run = forms.ChoiceField(choices=COMMAND_CHOICES,
        label="Command to run",
        widget=widgets.RadioSelect)
