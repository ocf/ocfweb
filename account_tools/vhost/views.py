from ocf.utils import user_attrs, user_is_group
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from vhost.forms import VirtualHostForm
from ocf.decorators import https_required, login_required, group_account_required
from django.core.urlresolvers import reverse
import datetime, socket

@login_required
@group_account_required
def request_vhost(request):
    user_account = request.session["ocf_user"]
    attrs = user_attrs(user_account)

    if request.method == "POST":
        form = VirtualHostForm(request.POST)

        if form.is_valid():
            # send email to hostmaster@ocf and redirect to success page
            requested_subdomain = form.cleaned_data["requested_subdomain"]
            requested_why = form.cleaned_data["requested_why"]
            your_name = form.cleaned_data["your_name"]
            your_email = form.cleaned_data["your_email"]
            your_position = form.cleaned_data["your_position"]

            full_domain = "{}.berkeley.edu".format(requested_subdomain)
            ip_addr = get_client_ip(request)

            try:
                ip_reverse = socket.gethostbyaddr(ip_addr)[0]
            except:
                ip_reverse = "unknown"

            subject = "Virtual Hosting Request: {} ({})".format(full_domain, user_account)
            message = (
                "Virtual Hosting Request:\n" + \
                "  - OCF Account: {user_account}\n" + \
                "  - OCF Account Title: {title}\n" + \
                "  - Requested Subdomain: {full_domain}\n" + \
                "  - Current URL: http://www.ocf.berkeley.edu/~{user_account}\n" + \
                "\n" + \
                "Request Reason:\n" + \
                "{requested_why}\n\n" + \
                "Requested by:\n" + \
                "  - Name: {your_name}\n" + \
                "  - Position: {your_position}\n" + \
                "  - Email: {your_email}\n" + \
                "  - IP Address: {ip_addr} ({ip_reverse})\n" + \
                "  - User Agent: {user_agent}\n" + \
                "\n\n" + \
                "--------\n" + \
                "Request submitted to account_tools ({hostname}) on {now}.\n" + \
                "{full_path}").format(
                    user_account=user_account,
                    title=attrs["cn"][0],
                    full_domain=full_domain,
                    requested_why=requested_why,
                    your_name=your_name,
                    your_position=your_position,
                    your_email=your_email,
                    ip_addr=ip_addr,
                    ip_reverse=ip_reverse,
                    user_agent=request.META.get("HTTP_USER_AGENT"),
                    now=datetime.datetime.now().strftime("%A %B %e, %Y @ %I:%M:%S %p"),
                    hostname=socket.gethostname(),
                    full_path=request.build_absolute_uri())

            from_addr = your_email
            to = ["ckuehl@ocf.berkeley.edu"]

            send_mail(subject, message, from_addr, to, fail_silently=False)
            return lol
    else:
        form = VirtualHostForm(initial={"requested_subdomain": user_account})

    group_url = "http://www.ocf.berkeley.edu/~{0}/".format(user_account)

    return render_to_response("request_vhost.html", {
        "form": form,
        "user": user_account,
        "attrs": attrs,
        "group_url": group_url
    }, context_instance=RequestContext(request))

# http://stackoverflow.com/a/5976065/450164
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip
