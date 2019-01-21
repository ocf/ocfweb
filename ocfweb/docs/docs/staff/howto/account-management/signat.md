[[!meta title="signat: check signatory status"]]

## Introduction

The `signat` script is used to look up the signatory status of people and
student groups. This allows us to verify that the people who email us or come
in to [[staff hours|staff-hours]] are really signatories for their group, and
it also gives all the information needed to create group accounts with
[[approve|doc staff/howto/user-services/approve]].

## How it works

`signat` is an interface to the [`ocflib`][ocflib] functions to query the
[CalLink API][callinkapi] for group signatories. `ocflib` is also used to look
up UIDs and OIDs in OCF [[LDAP|doc staff/backend/ldap]] and names in the
university's [LDAP directory service][berkeleyldap].

[ocflib]: github.com/ocf/ocflib
[callinkapi]: https://orapps.berkeley.edu/StudentGroupServiceV2/service.asmx
[berkeleyldap]: https://wikihub.berkeley.edu/display/calnet/LDAP+Directory+Service

## Usage

There are several different types of queries available through `signat`.

```text
$ signat -h
usage: signat [-h] {uid,oid,user,name,group} ...

Find active student groups and signatories

optional arguments:
  -h, --help            show this help message and exit

subcommands:

  {uid,oid,user,name,group}
    uid                 Look up the signatory status of a person by CalNet UID
    oid                 Look up the signatories of a group by CalLink OID
    user                Look up the signatory status of an OCF user
    name                Look up the signatory status of a person by name
    group               Look up the signatories of a group by group name
```

`group` and `name` are the easiest queries to use when a group or signatory
doesn't already have an OCF account. These perform a keyword search for people
or groups by name.

```text
$ signat name N Impicciche
Searching for people... Found 1 entry.
Searching for signatories...

NICHOLAS DANIEL IMPICCICHE (1032668)
====================================
Group                    Accounts                       OID
-----------------------  ---------------------------  -----
Open Computing Facility  decal, linux, ggroup, group  46187

$ signat group free
Searching for groups... Found 2 entries.
Searching for signatories...

Free Ventures (91915)
Group accounts: free
=====================
Signatory                   UID
----------------------  -------
KEYAN SARRAFZADEH       1004456
DAMINI SATIJA            995579
Jasmine Chiman STOY      995773
AMRIT MAHADEVAN AYALUR  1027142

Students for a Free Tibet at Berkeley (46707)
Group accounts: n/a
=============================================
Signatory               UID
------------------  -------
SANGMO TENZIN ARYA  1035554
DORJEE TASHI        1110958
TENZING DOLMA       1027935
```

`user` looks up an OCF account and prints the signatories for a group account
or the signatory status of an individual account.

```text
$ signat user nickimp
NICHOLAS DANIEL IMPICCICHE (1032668)
====================================
Group                    Accounts                       OID
-----------------------  ---------------------------  -----
Open Computing Facility  decal, linux, ggroup, group  46187

$ signat user free
Free Ventures (91915)
Group accounts: free
=====================
Signatory                   UID
----------------------  -------
KEYAN SARRAFZADEH       1004456
DAMINI SATIJA            995579
Jasmine Chiman STOY      995773
AMRIT MAHADEVAN AYALUR  1027142
```

The other two queries, `uid` and `oid`, don't offer much convenience, but
complete the spectrum of useful queries.

```text
$ signat uid 1032668
NICHOLAS DANIEL IMPICCICHE (1032668)
====================================
Group                    Accounts                       OID
-----------------------  ---------------------------  -----
Open Computing Facility  decal, linux, ggroup, group  46187

$ signat oid 91915
Free Ventures (91915)
Group accounts: free
=====================
Signatory                   UID
----------------------  -------
KEYAN SARRAFZADEH       1004456
DAMINI SATIJA            995579
Jasmine Chiman STOY      995773
AMRIT MAHADEVAN AYALUR  1027142
```
