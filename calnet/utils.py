try:
	from xml.etree import ElementTree
except ImportError:
	from elementtree import ElementTree

from urllib import urlencode, urlopen
from urlparse import urljoin
from django.conf import settings

def verify_ticket(ticket, service):
    """Verifies CAS 2.0+ XML-based authentication ticket.

    Returns CalNet UID on success and None on failure.
    """
    params = {'ticket': ticket, 'service': service}
    url = (urljoin(settings.CALNET_SERVER_URL, 'serviceValidate') + '?' +
           urlencode(params))
    try:
    	page = urlopen(url)
        response = page.read()
        tree = ElementTree.fromstring(response)
        if tree[0].tag.endswith('authenticationSuccess'):
            return tree[0][0].text
        else:
            return None
    except:
    	return None
