from django import forms

class VirtualHostForm(forms.Form):
    # group identity
    group_no_vhost = forms.BooleanField(
        label="We do not already have virtual hosting on our OCF account.")

    # requested subdomain
    requested_subdomain = forms.CharField(
        label="Requested Subdomain:",
        min_length=1,
        max_length=32)

    requested_subdomain_available = forms.BooleanField(
        label="We have verified that the requested subdomain is not \
               already in use.")

    requested_why = forms.CharField(
        widget=forms.Textarea,
        label="Please explain why you would like to use the requested \
               subdomain instead of your current address on \
               ocf.berkeley.edu.",
        min_length=1,
        max_length=1024)

    # web site requirements
    website_complete = forms.BooleanField(
        label="Our website is already complete and uploaded to the OCF \
               server. The website has the final content, and is not \
               just a placeholder.")

    website_hosted_by_ocf = forms.BooleanField(
        label="Our website is substantially hosted by the OCF. We do \
               not use frames, redirects, proxies, or other tricks to \
               circumvent this policy.")

    website_ocf_banner = forms.BooleanField(
        label="We have placed a \
                <a href=\"http://www.ocf.berkeley.edu/images/hosted-logos/\">\
                Hosted by the OCF</a> banner image on our site.")

    website_disclaimer_text = forms.BooleanField(
        label="We have placed the \
               <a href=\"http://wiki.ocf.berkeley.edu/services/vhost/#disclaimer\">\
               university-required disclaimer</a> on every page of our \
               site.")

    website_updated_software = forms.BooleanField(
        label="Any software (such as WordPress, Joomla, Drupal, etc.) \
               is fully updated, and we will commit to updating it \
               regularly to ensure our site is not compromised. (If \
               you are not using any software on your website, check \
               this box and move on.)")

    # confirm request
    your_name = forms.CharField(
        label="Your Full Name:",
        min_length=1,
        max_length=64)

    your_position = forms.CharField(
        label="Your Relationship to Group:",
        min_length=1,
        max_length=64)
