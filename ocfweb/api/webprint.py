# import random
# import string
# import subprocess
from django import forms
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from ocflib.printing.quota import get_connection
from ocflib.printing.quota import get_quota

from ocfweb.auth import login_required
from ocfweb.component.session import logged_in_user


class WebprintForm(forms.Form):
    """
    Fields for print request web form.
    """
    file_input = forms.FileField()
    n_copies = forms.IntegerField()
    print_type = forms.ChoiceField(choices=[('single', 'Single-sided'), ('double', 'Double-sided')])
    page_orientation = forms.ChoiceField(choices=[('portrait', 'Portrait'), ('landscape', 'Landscape')])


@require_POST
@login_required
def submit_print_request(request: HttpRequest) -> HttpResponse:
    """
    Submit a web printing request. Returns a print code.
    """
    try:
        user = logged_in_user(request)

        with get_connection() as c:
            # NOTE: this check happens when we run lp as well; just
            # running it pre-submission as well for the web version
            print_quota = get_quota(c, user)
            if print_quota.daily <= 0:
                return HttpResponseBadRequest('No remaining pages in daily print quota')

        form = WebprintForm(request.POST, request.FILES)
        if not form.is_valid():
            return HttpResponseBadRequest(form.errors.as_ul())

        # TODO: submit the print request

        # print_type, page_orientation = form.cleaned_data.get('print_type'), form.cleaned_data.get('page_orientation')

        # sidedness_opt: str
        # if print_type == 'single':
        #     sidedness_opt = 'sides=one-sided'
        # elif print_type == 'double':
        #     if page_orientation == 'portrait':
        #         sidedness_opt = 'sides=two-sided-long-edge'
        #     elif page_orientation == 'landscape':
        #         sidedness_opt = 'sides=two-sided-short-edge'

        # filename = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        # with open(f"/tmp/{filename}.pdf", "wb") as f:
        #     f.write(form.cleaned_data.get('file_input').read())

        # lp_cmd = ["lp", "-d", "printhost", "-n", str(form.cleaned_data['n_copies']),
        #           "-o", sidedness_opt, f"/tmp/{filename}.pdf"]
        # subprocess.run(lp_cmd, check=True)

        return HttpResponseRedirect(reverse('webprint-home'))

    except (KeyError, ValueError) as e:
        return HttpResponseBadRequest(e)


@require_POST
@login_required
def cancel_print_request(request: HttpRequest) -> HttpResponse:
    """
    Cancel a web printing request.
    """
    return HttpResponseBadRequest('Not implemented')
