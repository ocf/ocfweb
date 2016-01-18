from collections import namedtuple

from django.shortcuts import render_to_response
from django.template import RequestContext
from ocflib.account.search import user_attrs


class Term(namedtuple('Term', ['name', 'gms', 'sms'])):
    pass


class Officer(namedtuple('Officer', ['uid', 'name'])):
    pass


# Some of the earliest officers' accounts are nonexistant or belong to
# someone else now, so type out just those here.
MISSING_NAMES = {
    'adam': 'Adam Richter',
    'appel': 'Shannon Appel',
    'ctl': 'Case Larsen',
    'dpassage': 'David Paschich',
    'glass': 'Adam Glass',
    'jenni': 'Jennifer Snider',
    'rgm': 'Rob Menke',
    'shipley': 'Peter Shipley',
    'sls': 'Sam Shen',
}


def fill_officers(term):
    return Term(
        term.name,
        gms=list(map(officer_from_uid, term.gms)),
        sms=list(map(officer_from_uid, term.sms)),
    )


def officer_from_uid(uid):
    if uid in MISSING_NAMES:
        return Officer(uid, MISSING_NAMES[uid])
    else:
        return Officer(uid, user_attrs(uid)['cn'][0])


BOD_TERMS = list(map(fill_officers, [
    Term('Spring 1989', gms=['psb'], sms=['shipley']),
    Term('Fall 1989', gms=['psb'], sms=['ctl']),
    Term('Spring 1999', gms=['ctl'], sms=['sls']),
    Term('Summer 1990', gms=['psb'], sms=['glass']),
    Term('Fall 1990', gms=['appel'], sms=['rgm']),
    Term('Spring 1991', gms=['appel'], sms=['dpassage']),
    Term('Fall 1991', gms=['gwh'], sms=['cgd']),
    Term('Spring 1992', gms=['adam'], sms=['rsr', 'alanc']),
    Term('Summer 1992', gms=['davidf'], sms=['marco']),
    Term('Fall 1992', gms=['emarkp', 'dpassage', 'cgd'], sms=['kmorgan']),
    Term('Spring 1993', gms=['kmorgan'], sms=['marco']),
    Term('Fall 1993', gms=['kmorgan'], sms=['lars']),
    Term('Spring 1994', gms=['nevman'], sms=['ari']),
    Term('Summer 1994', gms=['nevman', 'kmorgan'], sms=['ari']),
    Term('Fall 1994', gms=['marco'], sms=['alanc']),
    Term('Spring 1995', gms=['jenni'], sms=['shyguy']),
    Term('Summer 1995', gms=['jenni'], sms=['erikm']),
    Term('Fall 1995', gms=['jenni'], sms=['erikm']),
    Term('Spring 1996', gms=['chaos'], sms=['mconst']),
    Term('Summer 1996', gms=['chaos'], sms=['jenni']),
    Term('Fall 1996', gms=['alanc'], sms=['jenni']),
    Term('Spring 1997', gms=['percival'], sms=['kennish']),
    Term('Summer 1997', gms=['chaos'], sms=['jenni']),
    Term('Fall 1997', gms=['runes'], sms=['kennish']),
    Term('Spring 1998', gms=['chaos'], sms=['ahilan']),
    Term('Summer 1998', gms=['chaos'], sms=['tee']),
    Term('Fall 1998', gms=['dunnthat'], sms=['katster']),
    Term('Spring 1999', gms=['dunnthat'], sms=['katster']),
    Term('Summer 1999', gms=['dunnthat'], sms=['katster']),
    Term('Fall 1999', gms=['jones', 'kenao'], sms=['katster', 'akopps']),
    Term('Spring 2000', gms=['smcc'], sms=['akopps']),
    Term('Fall 2000', gms=['cpfeyh', 'smcc'], sms=['akopps']),
    Term('Spring 2001', gms=['gmg'], sms=['smcc', 'akopps']),
    Term('Fall 2001', gms=['gmg'], sms=['smcc', 'ajan']),
    Term('Spring 2002', gms=['calman'], sms=['smcc', 'wyc']),
    Term('Fall 2002', gms=['ewhatt', 'wyc'], sms=['akopps', 'dwc']),
    Term('Spring 2003', gms=['jeffe', 'cpfeyh'], sms=['dwc', 'aoshi']),
    Term('Fall 2003', gms=['jkit', 'eleen'], sms=['jones', 'akopps']),
    Term('Spring 2004', gms=['eleen'], sms=['jkit']),
    Term('Fall 2004', gms=['eleen'], sms=['jkit', 'geo']),
    Term('Spring 2005', gms=['frank', 'brando'], sms=['jerjou', 'dima']),
    Term('Fall 2005', gms=['frank'], sms=['elliot']),
    Term('Spring 2006', gms=['tdhock', 'griffin'], sms=['sluo']),
    Term('Fall 2006', gms=['thomson', 'akit'], sms=['sle', 'yury']),
    Term('Spring 2007', gms=['akit', 'sahnn'], sms=['aoaks', 'elliot']),
    Term('Fall 2007', gms=['akit'], sms=['wjm', 'sluo', 'jchu']),
    Term('Spring 2008', gms=['gordeon'], sms=['gfs']),
    Term('Fall 2008', gms=['gcwong'], sms=['mgasidlo', 'jchu']),
    Term('Spring 2009', gms=['gcwong'], sms=['mgasidlo', 'jameson']),
    Term('Fall 2009', gms=['mgasidlo'], sms=['sanjayk', 'alanw']),
    Term('Spring 2010', gms=['mgasidlo'], sms=['sanjayk', 'alanw']),
    Term('Fall 2010', gms=['sherryg', 'simplyhd'], sms=['sanjayk', 'waf']),
    Term('Spring 2011', gms=['sherryg'], sms=['daradib', 'benortiz']),
    Term('Summer 2011', gms=['sherryg'], sms=['daradib', 'benortiz']),
    Term('Fall 2011', gms=['daradib'], sms=['waf', 'kedo']),
    Term('Spring 2012', gms=['daradib', 'mcint'], sms=['waf', 'kedo']),
    Term('Summer 2012', gms=['daradib'], sms=['waf']),
    Term('Fall 2012', gms=['daradib'], sms=['tzhu', 'sanjayk']),
    Term('Spring 2013', gms=['daradib'], sms=['tzhu', 'waf']),
    Term('Summer 2013', gms=['daradib'], sms=['tzhu']),
    Term('Fall 2013', gms=['daradib'], sms=['tzhu']),
    Term('Spring 2014', gms=['nickimp'], sms=['ckuehl']),
    Term('Fall 2014', gms=['nickimp'], sms=['ckuehl']),
    Term('Spring 2015', gms=['nickimp'], sms=['ckuehl']),
    Term('Fall 2015', gms=['nickimp'], sms=['ckuehl']),
]))


def officers(doc, request):
    return render_to_response(
        'officers.html',
        {
            'title': doc.title,
            'current_term': BOD_TERMS[-1],
            'previous_terms': BOD_TERMS[:-1],
        },
        context_instance=RequestContext(request),
    )
