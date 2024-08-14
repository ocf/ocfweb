import math
from dataclasses import dataclass
from datetime import date
from typing import Any
from typing import Callable
from typing import cast
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from ocflib.account.search import user_attrs

from ocfweb import caching

OfficerUidOrInfo = Union[str, Tuple[str, date, date], Tuple[str, date, date, bool]]


@dataclass
class Committee:
    name: str
    heads: 'List[Officer]'


@dataclass
class Term:
    name: str
    gms: 'List[Officer]'
    sms: 'List[Officer]'
    dgms: 'List[Officer]'
    dsms: 'List[Officer]'
    heads: List[Committee]

    def __init__(
        self,
        name: str,
        gms: List[OfficerUidOrInfo],
        sms: List[OfficerUidOrInfo],
        dgms: Optional[List[OfficerUidOrInfo]] = None,
        dsms: Optional[List[OfficerUidOrInfo]] = None,
        heads: Optional[List[Tuple[str, List[OfficerUidOrInfo]]]] = None,
    ):
        self.name = name
        self.gms = list(map(Officer.from_uid_or_info, gms))
        self.sms = list(map(Officer.from_uid_or_info, sms))
        self.dgms = list(map(Officer.from_uid_or_info, dgms or []))
        self.dsms = list(map(Officer.from_uid_or_info, dsms or []))
        self.heads = [
            Committee(committee[0], list(map(Officer.from_uid_or_info, committee[1])))
            for committee in heads or []
        ]


@dataclass
class Officer:
    uid: str
    name: str
    start: Optional[date]
    end: Optional[date]
    acting: bool

    @classmethod
    def from_uid_or_info(cls: 'Callable[..., Officer]', uid_or_info: OfficerUidOrInfo) -> 'Officer':
        start: Optional[date]
        end: Optional[date]

        if isinstance(uid_or_info, tuple):
            if len(uid_or_info) == 3:
                uid, start, end = cast(Tuple[str, date, date], uid_or_info)
                acting = False
            else:
                uid, start, end, acting = cast(Tuple[str, date, date, bool], uid_or_info)
        else:
            uid = uid_or_info
            start = end = None
            acting = False

        name = MISSING_NAMES.get(uid)
        if not name:
            name, = user_attrs(uid)['cn']
        return cls(uid=uid, name=name, start=start, end=end, acting=acting)

    @property
    def full_term(self) -> bool:
        return self.start is None and self.end is None

    def __str__(self) -> str:
        s = f'{self.name} <{self.uid}>'
        if self.acting:
            if self.end is not None and self.end < date(2016, 11, 14):
                # Prior to the 2016 constitution, we had interim managers
                # during vacancies, rather than acting managers
                s += ' (interim)'
            else:
                s += ' (acting)'
        if not self.full_term:
            assert self.start is not None
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
    # temporary fix for lengthy ldap calls
    'abizer': 'Abizer Lokhandwala',
    'adi': 'Aditya Mangalampalli',
    'ahilan': 'Ahilan Anantha',
    'ajani': 'Bem Ajani Jones-Bey',
    'akit': 'Angel Kittiyachavalit',
    'akopps': 'Akop Pogosian',
    'alanc': 'Alan Coopersmith',
    'alanw': 'Alan Wong',
    'aly': 'Albert Ye',
    'anddone': 'Andrei Dones',
    'anirudhsuresh': 'Anirudh Suresh',
    'aoaks': 'Aaron Oaks',
    'aoshi': 'Randy Aoshi Chung',
    'ari': 'Ari Zilka',
    'asai': 'Andrew Aikawa',
    'awelty': 'Alexander Byron Welty',
    'baisang': 'Brian Sang',
    'bencuan': 'Ben Cuan',
    'benortiz': 'Benjamin Eugene Ortiz',
    'bernardzhao': 'Bernard Zhao',
    'bplate': 'Ben Plate',
    'brando': 'Brandon Jue',
    'bryli': 'Bryan Li',
    'btorres': 'Benjamin Torres',
    'bzh': 'Benjamin Zhang',
    'calman': 'Stephen J. Callahan',
    'cgd': 'Chris G. Demetriou',
    'chaos': 'Elaine Chao',
    'ckuehl': 'Chris Kuehl',
    'cooperc': 'Christopher Cooper',
    'cpfeyh': 'Charles Patrick Feyh',
    'dapark': 'Darlnim Park',
    'daradib': 'Dara Adib',
    'davidf': 'David Friedman',
    'dima': 'Dmitriy Shirchenko',
    'dkessler': 'Daniel Kessler',
    'dphan': 'Derek Phan',
    'dunnthat': 'Richard Dunn',
    'dwc': 'Derek Chan',
    'eleen': 'Eleen Chiang',
    'elliot': 'Elliot Block',
    'emarkp': 'E. Mark Ping',
    'ericyang': 'Eric Yang',
    'erikm': 'Erik Muller',
    'ethanhs': 'Ethan Smith',
    'ethanhu': 'Ethan Hu',
    'etw': 'Ethan Wu',
    'ewhatt': 'Emily Watt',
    'exiang': 'Edric Xiang',
    'frank': 'Frank Joseph Cohen',
    'fydai': 'Frank Dai',
    'gcwong': 'Genevieve C Wong',
    'geo': 'George Wu',
    'gfs': 'Gregory Francis Shuflin',
    'gmg': 'Gabriel Gonzalez',
    'gordeon': 'Gordon Mei',
    'griffin': 'Griffin Foster',
    'gwh': 'George William Herbert',
    'hexhu': 'Leo Huang',
    'idham': 'Ishaan Dham',
    'inurzhanov': 'Isabelle Nurzhanov',
    'jameson': 'Jameson J Lee',
    'jaw': 'Ja (Thanakul) Wattanawong',
    'jaysa': 'Jaysa Garcia',
    'jchu': 'Jonathan Rich Chu (milki)',
    'jeffe': 'Jeff Emrich',
    'jenni': 'Jennifer Coopersmith',
    'jerjou': 'Jerjou Cheng',
    'jkit': 'Jimmy Kittiyachavalit',
    'jones': 'Devin Jones',
    'jvperrin': 'Jason Perrin',
    'jyxzhang': 'Justin Zhang',
    'katster': 'Katrina Templeton',
    'kedo': 'Kenneth Hui Do',
    'kenao': 'Kenneth Ott',
    'kennish': 'Kenneth Nishimoto',
    'keur': 'Kevin Kuehler',
    'kian': 'Kian Sutarwala',
    'kmo': 'Kevin Mo',
    'kmorgan': 'Keir Morgan',
    'kpengboy': 'Kevin Peng',
    'kuoh': 'Harrison Kuo',
    'laksith': 'Laksith Venkatesh Prabu',
    'lars': 'Lars Smith',
    'lmathias': 'Lance Mathias',
    'lemurseven': 'Michael Lisano',
    'lukepeters': 'Luke Peters',
    'marco': 'Marco Nicosia',
    'mattmcal': 'Matthew McAllister',
    'mcint': 'Loren Patrick McIntyre',
    'mconst': 'Michael Constant',
    'mgasidlo': 'Michael Shimei Gasidlo',
    'ncberberi': 'Nicholas Berberi',
    'ncograin': 'Nikhil Ograin',
    'nevman': 'Nevin Cheung',
    'nickimp': 'Nick Impicciche',
    'nint': 'Brian Blair',
    'njha': 'Nikhil Jha',
    'oliverni': 'Oliver Ni',
    'percival': 'John W. Percival',
    'php': 'Patricia Hanus',
    'psb': 'Partha S. Banerjee',
    'rachy': 'Rachel Trujillo',
    'rayh': 'Raymond Huang',
    'ronitnath': 'Ronit Nath',
    'rrchan': 'Ryan-chan',
    'rsr': 'Roy S. Rapoport',
    'runes': 'Rune Stromsness',
    'sahnn': 'Sue Hyun Ahnn',
    'sanjayk': 'Sanjay Krishnan',
    'shasan': 'Sahil Hasan',
    'sherryg': 'Sherry Ann Gong',
    'shyguy': 'David Shih',
    'simplyhd': 'Huy The Doan',
    'sle': 'Stephen Le',
    'sluo': 'Steven Yuifai Luo',
    'smcc': 'Stephen McCamant',
    'snarain': 'Saurabh Narain',
    'storce': 'Joseph Wang',
    'tdhock': 'Toby Hocking',
    'tee': 'Luns Tee',
    'thomson': 'Thomson Van Nguyen',
    'trinityc': 'Trinity Chung',
    'trliu': 'Tony Liu',
    'tzhu': 'Timmy Zhu',
    'waf': 'Felix Andy Wong',
    'wjm': 'William Mallard',
    'wqnguyen': 'Wilson Nguyen',
    'wyc': 'Wayne Yu-Wing Chan',
    'yehchanyoo': 'Yehchan Yoo',
    'yury': 'Yury Arkady Sobolev',
}


# This function makes approximately five million LDAP queries, so it's
# important that these terms aren't loaded at import time.
@caching.periodic(math.inf)
def _bod_terms() -> List[Term]:
    return [
        Term(
            'Spring 1989',
            gms=[('psb', date(1989, 4, 6), date(1989, 11, 14))],
            sms=[('shipley', date(1989, 4, 6), date(1989, 11, 14))],
        ),
        Term(
            'Fall 1989',
            gms=[('psb', date(1989, 11, 14), date(1990, 3, 21))],
            sms=[('ctl', date(1989, 11, 14), date(1990, 3, 21))],
        ),
        Term('Spring 1990', gms=['ctl'], sms=['sls']),
        Term('Summer 1990', gms=['psb'], sms=['glass']),
        Term('Fall 1990', gms=['appel'], sms=['rgm']),
        Term('Spring 1991', gms=['appel'], sms=['dpassage']),
        Term('Fall 1991', gms=['gwh'], sms=['cgd']),
        Term(
            'Spring 1992',
            gms=['adam'],
            sms=[
                ('rsr', date(1992, 2, 6), date(1992, 4, 16)),
                ('alanc', date(1992, 4, 16), date(1992, 4, 23), True),
                ('rsr', date(1992, 4, 23), date(1992, 9, 10)),
            ],
        ),
        Term('Summer 1992', gms=['davidf'], sms=['marco']),
        Term(
            'Fall 1992',
            gms=[
                ('emarkp', date(1992, 9, 10), date(1992, 10, 29)),
                ('dpassage', date(1992, 10, 29), date(1992, 11, 12), True),
                ('cgd', date(1992, 11, 12), date(1993, 2, 4)),
            ],
            sms=['kmorgan'],
        ),
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
        Term(
            'Fall 1999',
            gms=['jones', 'kenao'],
            sms=[
                ('katster', date(1999, 9, 8), date(1999, 11, 17)),
                ('akopps', date(1999, 11, 17), date(2000, 1, 31), True),
            ],
        ),
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
        Term(
            'Fall 2007',
            gms=['akit'],
            sms=[
                ('wjm', date(2007, 9, 13), date(2007, 10, 4)),
                ('sluo', date(2007, 10, 4), date(2007, 10, 11), True),
                ('jchu', date(2007, 10, 11), date(2008, 2, 7)),
            ],
        ),
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
        Term(
            'Fall 2016',
            gms=['nickimp'],
            sms=['jvperrin', 'mattmcal'],
            dgms=[
                ('baisang', date(2016, 9, 26), date(2016, 11, 28)),
                ('shasan', date(2016, 10, 24), date(2016, 11, 28)),
            ],
        ),
        Term(
            'Spring 2017', gms=['nickimp', 'baisang'], sms=['jvperrin', 'mattmcal'],
            dgms=['shasan'], dsms=['kpengboy'],
        ),
        Term(
            'Fall 2017', gms=['baisang', 'shasan'], sms=['jvperrin', 'abizer'],
            dgms=['asai'], dsms=['dkessler', 'kuoh'],
        ),
        Term(
            'Spring 2018', gms=['shasan'], sms=['jvperrin', 'abizer'],
            dgms=['asai', 'awelty', 'baisang'], dsms=['dkessler', 'kuoh'],
        ),
        Term(
            'Fall 2018',
            gms=[
                ('asai', date(2018, 5, 12), date(2018, 11, 7)),
                ('awelty', date(2018, 11, 7), date(2018, 11, 26), True),
                ('trliu', date(2018, 11, 7), date(2018, 11, 26), True),
                ('awelty', date(2018, 11, 26), date(2018, 12, 14)),
                ('trliu', date(2018, 11, 26), date(2018, 12, 14)),
            ],
            sms=['dkessler', 'keur'],
        ),
        Term(
            'Spring 2019', gms=['abizer', 'awelty'], sms=['bzh', 'dkessler'],
            dgms=['asai'], dsms=['ethanhs', 'cooperc'],
        ),
        Term(
            'Fall 2019',
            gms=['cooperc', 'php'],
            sms=[
                ('ethanhs', date(2019, 5, 18), date(2019, 11, 18)),
                'fydai',
            ],
        ),
        Term(
            'Spring 2020',
            gms=['dphan', 'bernardzhao'],
            sms=['cooperc', 'jaw'],
            heads=[
                ('University Affairs', ['dphan', 'bernardzhao']),
                ('Internal', ['php', 'kmo']),
                ('Industry and Alumni Relations', ['asai', 'rachy']),
                ('Finance', ['ncberberi', 'nint']),
                (
                    'Communications', [
                        ('rachy', date(2019, 12, 21), date(2020, 3, 8)),
                        ('snarain', date(2020, 3, 30), date(2020, 4, 6), True),
                        ('snarain', date(2020, 4, 6), date(2020, 5, 15)),
                    ],
                ),
                ('DeCal', ['exiang', 'bencuan', 'kmo']),
            ],
        ),
        Term(
            'Fall 2020',
            gms=['dphan', 'kmo'],
            sms=['fydai', 'jaw'],
            heads=[
                ('University Affairs', ['dphan', 'kmo']),
                ('Internal', ['wqnguyen', 'snarain']),
                ('Industry and Alumni Relations', ['bernardzhao']),
                ('Finance', ['ncberberi']),
                ('Communications', ['snarain', 'nint']),
                ('DeCal', ['njha', 'bencuan', 'bernardzhao']),
            ],
        ),
        Term(
            'Spring 2021',
            gms=['kmo', 'snarain'],
            sms=['njha', 'fydai'],
            heads=[
                ('Internal', ['jaw', 'ronitnath']),
                ('Industry and Alumni Relations', ['rrchan', 'asai']),
                ('Finance', ['ncberberi', 'ronitnath']),
                ('Communications', ['bencuan', 'ronitnath']),
                ('DeCal', ['bencuan', 'hexhu']),
            ],
        ),
        Term(
            'Fall 2021',
            gms=['snarain', 'ncberberi'],
            sms=['ethanhs', 'njha'],
            heads=[
                ('Internal', ['rjz', 'ronitnath']),
                ('Industry and Alumni Relations', ['kmo']),
                ('Finance', ['rayh', 'ronitnath']),
                ('Communications', ['rjz', 'jyxzhang']),
                ('DeCal', ['bencuan']),
            ],
        ),
        Term(
            'Spring 2022',
            gms=['jyxzhang', 'bencuan'],
            sms=['rjz', 'etw'],
            heads=[
                ('Internal', ['kian', 'bryli']),
                ('External', ['ncograin', 'anddone']),
                ('Finance', ['snarain', 'rayh', 'ncberberi']),
                ('DeCal', ['lmathias', 'laksith']),
            ],
        ),
        Term(
            'Fall 2022',
            gms=['jyxzhang', 'njha'],
            sms=['rjz', 'etw'],
            heads=[
                ('Internal', ['kian', 'bryli', 'bencuan']),
                ('External', ['anddone']),
                ('Finance', ['snarain', 'bencuan']),
                ('DeCal', ['lmathias', 'laksith', 'idham']),
            ],
        ),
        Term(
            'Spring 2023',
            gms=['kian', 'ncograin'],
            sms=['etw', 'njha'],
            heads=[
                ('Internal', ['ericyang', 'ethanhu', 'dapark']),
                ('External', ['anddone', 'ethanhu', 'btorres']),
                ('Finance', ['adi', 'rjz', 'trinityc']),
                ('DeCal', ['laksith', 'lmathias', 'idham']),
            ],
        ),
        Term(
            'Fall 2023',
            gms=['dapark', 'jaysa'],
            sms=['oliverni', 'rjz'],
            heads=[
                ('Internal', ['bryli', 'trinityc', 'yehchanyoo']),
                ('External', ['anddone', 'btorres', 'ethanhu']),
                ('Finance', ['adi', 'anirudhsuresh', 'yehchanyoo']),
                ('DeCal', ['adi', 'btorres', 'trinityc']),
            ],
        ),
        Term(
            'Spring 2024',
            gms=['bryli', 'ronitnath'],
            sms=['oliverni', 'njha'],
            heads=[
                ('Internal', ['adi']),
                ('External', ['inurzhanov']),
                ('Finance', ['anirudhsuresh']),
                ('DeCal', ['jaysa', 'kian']),
            ],
        ),
        Term(
            'Fall 2024',
            gms=['jaysa', 'rjz'],
            sms=['oliverni', 'lemurseven'],
            heads=[
                ('Internal', ['storce', 'lukepeters']),
                ('Finance', ['adi']),
                ('DeCal', ['kian', 'aly']),
            ],
        ),
    ]


def officers(doc: Any, request: HttpRequest) -> HttpResponse:
    terms = _bod_terms()
    return render(
        request,
        'docs/officers.html',
        {
            'title': doc.title,
            'current_term': terms[-1],
            'previous_terms': terms[-2::-1],
        },
    )
