from ocf.utils import user_attrs, user_is_group, check_email
from django.conf import settings
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.mail import send_mail
from vhost.forms import VirtualHostForm
from ocf.decorators import login_required, group_account_required
from django.core.urlresolvers import reverse
import dns.resolver as resolver
import datetime, socket, email, os.path

@login_required
@group_account_required
def request_vhost(request):
    user_account = request.session["ocf_user"]
    attrs = user_attrs(user_account)
    error = None

    if has_vhost(user_account):
        return render_to_response("already_have_vhost.html", {"user": user_account})

    if request.method == "POST":
        form = VirtualHostForm(request.POST)

        if form.is_valid():
            requested_subdomain = form.cleaned_data["requested_subdomain"]
            requested_why = form.cleaned_data["requested_why"]
            comments = form.cleaned_data["comments"]
            your_name = form.cleaned_data["your_name"]
            your_email = form.cleaned_data["your_email"]
            your_position = form.cleaned_data["your_position"]

            full_domain = "{}.berkeley.edu".format(requested_subdomain)

            # verify that the requested domain is available
            if not domain_available(full_domain):
                error = "The domain you requested is not available. Please select a different one."

            if not check_email(your_email):
                error = "The email you entered doesn't appear to be valid. Please double-check it."

            if not error:
                # send email to hostmaster@ocf and redirect to success page
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
                    "  - Current URL: http://www.ocf.berkeley.edu/~{user_account}/\n" + \
                    "\n" + \
                    "Request Reason:\n" + \
                    "{requested_why}\n\n" + \
                    "Comments/Special Requests:\n" + \
                    "{comments}\n\n" + \
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
                        comments=comments,
                        your_name=your_name,
                        your_position=your_position,
                        your_email=your_email,
                        ip_addr=ip_addr,
                        ip_reverse=ip_reverse,
                        user_agent=request.META.get("HTTP_USER_AGENT"),
                        now=datetime.datetime.now().strftime("%A %B %e, %Y @ %I:%M:%S %p"),
                        hostname=socket.gethostname(),
                        full_path=request.build_absolute_uri())

                from_addr = email.utils.formataddr((your_name, your_email))
                to = ["hostmaster@ocf.berkeley.edu"]

                try:
                    send_mail(subject, message, from_addr, to, fail_silently=False)
                    return redirect(reverse("request_vhost_success"))
                except Exception as ex:
                    print ex
                    print("Failed to send vhost request email!")
                    error = \
                        "We were unable to submit your virtual hosting request. Please " + \
                        "try again or email us at hostmaster@ocf.berkeley.edu"
    else:
        form = VirtualHostForm(initial={"requested_subdomain": user_account})

    group_url = "http://www.ocf.berkeley.edu/~{0}/".format(user_account)

    return render_to_response("request_vhost.html", {
        "form": form,
        "user": user_account,
        "attrs": attrs,
        "group_url": group_url,
        "error": error
    }, context_instance=RequestContext(request))

def request_vhost_success(request):
    return render_to_response("successfully_submitted_vhost.html")

# http://stackoverflow.com/a/5976065/450164
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip

def domain_available(domain):
    try:
        resolver.query(domain, "NS")
    except resolver.NXDOMAIN:
        return True
    except:
        pass
    return False

def has_vhost(user):
    """Returns whether or not a virtual host is already configured for
    the given user."""

    check = (user, user + "!")
    line_matches = lambda fields: len(fields) > 0 and fields[0] in check

    with open(os.path.expanduser(settings.OCF_VHOST_DB)) as file:
        return any(line_matches(line.split()) for line in file)
