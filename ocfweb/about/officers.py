from collections import defaultdict
from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple

from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from ocflib.account.officers import all_officer_roles

from ocfweb import caching


@dataclass
class Committee:
    name: str
    heads: 'List[Officer]'


@dataclass
class Officer:
    uid: str
    name: str

    def __str__(self) -> str:
        return f'{self.name} <{self.uid}>'


@dataclass
class Term:
    name: str
    gms: List[Officer]
    sms: List[Officer]
    dgms: List[Officer]
    dsms: List[Officer]
    heads: List[Committee]

    def __init__(
        self,
        name: str,
        gms: List[Officer],
        sms: List[Officer],
        dgms: Optional[List[Officer]] = None,
        dsms: Optional[List[Officer]] = None,
        heads: Optional[List[Tuple[str, List[Officer]]]] = None,
    ):
        self.name = name
        self.gms = gms
        self.sms = sms
        self.dgms = dgms or []
        self.dsms = dsms or []
        self.heads = [
            Committee(committee_name, officers)
            for committee_name, officers in heads or []
        ]


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


MISSING_ROLES = [
    ('shipley', 'sm', 'Spring 1989'),
    ('ctl', 'sm', 'Fall 1989'),
    ('ctl', 'gm', 'Spring 1990'),
    ('sls', 'sm', 'Spring 1990'),
    ('glass', 'sm', 'Summer 1990'),
    ('appel', 'gm', 'Fall 1990'),
    ('rgm', 'sm', 'Fall 1990'),
    ('appel', 'gm', 'Spring 1991'),
    ('dpassage', 'sm', 'Spring 1991'),
    ('adam', 'gm', 'Spring 1992'),
    ('dpassage', 'gm', 'Fall 1992'),
]


def _term_sort_key(term: str) -> Tuple[int, int]:
    season, year = term.split()
    return int(year), ('Spring', 'Summer', 'Fall').index(season)


def _bod_terms() -> List[Term]:
    officer_roles = all_officer_roles()
    names: Dict[str, str] = dict(MISSING_NAMES)
    for r in officer_roles:
        names.setdefault(r.uid, r.name)
    officer_cache: Dict[str, Officer] = {}

    def officer(uid: str) -> Officer:
        if uid not in officer_cache:
            officer_cache[uid] = Officer(uid=uid, name=names[uid])
        return officer_cache[uid]

    roles = [(r.uid, r.role, r.term, r.committee) for r in officer_roles]
    roles.extend((uid, role, term, None) for uid, role, term in MISSING_ROLES)

    by_role: Dict[str, Dict[str, Set[str]]] = defaultdict(lambda: defaultdict(set))
    heads: Dict[str, Dict[str, Set[str]]] = defaultdict(lambda: defaultdict(set))
    for uid, role, term, committee in roles:
        if role == 'head':
            heads[term][committee].add(uid)
        else:
            by_role[term][role].add(uid)

    return [
        Term(
            term,
            gms=[officer(u) for u in sorted(by_role[term]['gm'])],
            sms=[officer(u) for u in sorted(by_role[term]['sm'])],
            dgms=[officer(u) for u in sorted(by_role[term]['dgm'])],
            dsms=[officer(u) for u in sorted(by_role[term]['dsm'])],
            heads=[
                (committee, [officer(u) for u in sorted(uids)])
                for committee, uids in sorted(heads[term].items())
            ],
        )
        for term in sorted(set(by_role) | set(heads), key=_term_sort_key)
    ]


def officers(request: HttpRequest) -> HttpResponse:
    terms = _bod_terms()
    return render(
        request,
        'about/officers.html',
        {
            'title': 'Officers',
            'current_term': terms[-1],
            'previous_terms': terms[-2::-1],
        },
    )
