import math
from collections import namedtuple
from datetime import date

from django.shortcuts import render
from ocflib.account.search import user_attrs

from ocfweb import caching


_Term = namedtuple('_Term', ['name', 'gms', 'sms', 'dgms', 'dsms'])


def Term(name, gms, sms, dgms=None, dsms=None):
    gms = list(map(Officer.from_uid_or_info, gms))
    sms = list(map(Officer.from_uid_or_info, sms))
    dgms = list(map(Officer.from_uid_or_info, dgms or []))
    dsms = list(map(Officer.from_uid_or_info, dsms or []))
    return _Term(name, gms, sms, dgms, dsms)


class Officer(namedtuple('Officer', ['uid', 'name', 'start', 'end', 'acting'])):

    @classmethod
    def from_uid_or_info(cls, uid_or_info):
        if isinstance(uid_or_info, tuple):
            if len(uid_or_info) == 3:
                uid, start, end = uid_or_info
                acting = False
            else:
                uid, start, end, acting = uid_or_info
        else:
            uid = uid_or_info
            start = end = None
            acting = False

        name = MISSING_NAMES.get(uid)
        if not name:
            name, = user_attrs(uid)['cn']
        return cls(uid=uid, name=name, start=start, end=end, acting=acting)

    @property
    def full_term(self):
        return self.start is None and self.end is None

    def __str__(self):
        s = '{} <{}>'.format(self.name, self.uid)
        if self.acting:
            if self.end is not None and self.end < date(2016, 11, 14):
                # Prior to the 2016 constitution, we had interim managers
                # during vacancies, rather than acting managers
                s += ' (interim)'
            else:
                s += ' (acting)'
        if not self.full_term:
            s += ' ({}–{})'.format(
                self.start.strftime('%m/%d/%y'),
                self.end.strftime('%m/%d/%y') if self.end is not None else '',
            )
        return s


# Some of the earliest officers' accounts are nonexistent or belong to
# someone else now, so type out just those here.
MISSING_NAMES = {
    'adam': 'Adam Richter',
    'appel': 'Shannon Appel',
    'ctl': 'Case Larsen',
    'dpassage': 'David Paschich',
    'glass': 'Adam Glass',
    'rgm': 'Rob Menke',
    'shipley': 'Peter Shipley',
    'sls': 'Sam Shen',
}


# This function makes approximately five million LDAP queries, so it's
# important that these terms aren't loaded at import time.
@caching.periodic(math.inf)
def _bod_terms():
    return [
        Term('Spring 1989',
             gms=[('psb', date(1989, 4, 6), date(1989, 11, 14))],
             sms=[('shipley', date(1989, 4, 6), date(1989, 11, 14))]),
        Term('Fall 1989',
             gms=[('psb', date(1989, 11, 14), date(1990, 3, 21))],
             sms=[('ctl', date(1989, 11, 14), date(1990, 3, 21))]),
        Term('Spring 1990', gms=['ctl'], sms=['sls']),
        Term('Summer 1990', gms=['psb'], sms=['glass']),
        Term('Fall 1990', gms=['appel'], sms=['rgm']),
        Term('Spring 1991', gms=['appel'], sms=['dpassage']),
        Term('Fall 1991', gms=['gwh'], sms=['cgd']),
        Term('Spring 1992',
             gms=['adam'],
             sms=[('rsr', date(1992, 2, 6), date(1992, 4, 16)),
                  ('alanc', date(1992, 4, 16), date(1992, 4, 23), True),
                  ('rsr', date(1992, 4, 23), date(1992, 9, 10))]),
        Term('Summer 1992', gms=['davidf'], sms=['marco']),
        Term('Fall 1992',
             gms=[('emarkp', date(1992, 9, 10), date(1992, 10, 29)),
                  ('dpassage', date(1992, 10, 29), date(1992, 11, 12), True),
                  ('cgd', date(1992, 11, 12), date(1993, 2, 4))],
             sms=['kmorgan']),
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
        Term('Fall 1999',
             gms=['jones', 'kenao'],
             sms=[('katster', date(1999, 9, 8), date(1999, 11, 17)),
                  ('akopps', date(1999, 11, 17), date(2000, 1, 31), True)]),
        Term('Spring 2000', gms=['smcc'], sms=['akopps']),
        Term('Fall 2000', gms=['cpfeyh', 'smcc'], sms=['akopps']),
        Term('Spring 2001', gms=['gmg'], sms=['smcc', 'akopps']),
        Term('Fall 2001', gms=['gmg'], sms=['smcc', 'ajani']),
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
        Term('Fall 2007',
             gms=['akit'],
             sms=[('wjm', date(2007, 9, 13), date(2007, 10, 4)),
                  ('sluo', date(2007, 10, 4), date(2007, 10, 11), True),
                  ('jchu', date(2007, 10, 11), date(2008, 2, 7))]),
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
        Term('Summer 2014', gms=['nickimp'], sms=['ckuehl']),
        Term('Fall 2014', gms=['nickimp'], sms=['ckuehl']),
        Term('Spring 2015', gms=['nickimp'], sms=['ckuehl']),
        Term('Summer 2015', gms=['nickimp'], sms=['ckuehl']),
        Term('Fall 2015', gms=['nickimp'], sms=['ckuehl']),
        Term('Spring 2016', gms=['nickimp'], sms=['jvperrin', 'mattmcal']),
        Term('Summer 2016', gms=['nickimp'], sms=['jvperrin', 'mattmcal']),
        Term('Fall 2016',
             gms=['nickimp'],
             sms=['jvperrin', 'mattmcal'],
             dgms=[('baisang', date(2016, 9, 26), date(2016, 11, 28)),
                   ('shasan', date(2016, 10, 24), date(2016, 11, 28))]),
        Term('Spring 2017', gms=['nickimp', 'baisang'], sms=['jvperrin', 'mattmcal'],
             dgms=['shasan'], dsms=['kpengboy']),
        Term('Fall 2017', gms=['baisang', 'shasan'], sms=['jvperrin', 'abizer']),
    ]


def officers(doc, request):
    terms = _bod_terms()
    return render(
        request,
        'docs/officers.html',
        {
            'title': doc.title,
            'current_term': terms[-1],
            'previous_terms': terms[:-1],
        },
    )
