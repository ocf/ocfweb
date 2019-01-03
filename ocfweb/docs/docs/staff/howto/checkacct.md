[[!meta title="checkacct: find accounts by full name"]]

## Introduction

If a member does not know their account name, you can use this script to look
it up.

Before recording an account request for a group with [[approve|doc
staff/scripts/approve]], check to see if the group already has an account. Be
sure to use different forms and abbreviations of the group's name to maximize
the chance that a group will be found.

This script will search [[LDAP|doc staff/backend/ldap]] for case-insensitive
matches in any part of the full name or account name, including part of a word.
For example, `checkacct wa fel andy` will search for any account that has "wa"
(as in waf), "fel" (as in Felix), and "andy" (as in Andy) in the full name
(LDAP cn) or account name (LDAP uid).

## Usage

    $ checkacct wa fel andy
    Login: waf                  Name: Felix Andy Wong

    $ checkacct dara
    Login: darac                Name: Dara T. Chu
    Login: laktalk              Name: Lakshmi Sridaran
    Login: sby                  Name: Sanji Bandara Yapa
    Login: angeloq              Name: Cesar Angelo Quindara
    Login: jayasund             Name: Jayasree Padma Sundaram
    Login: dpastor              Name: Dara Elana Pastor
    Login: msiva                Name: Matheepan Sivagnanasundaram
    Login: daraech              Name: Diana Darae Choe
    Login: suchitha             Name: Suchitha Sundaram
    Login: csavong              Name: Christindaravy Savong
    Login: norac                Name: Nora Chandara
    Login: salmabah             Name: Salma Bahadarakhann
    Login: darabkin             Name: David Andrew Rabkin
    Login: daradib              Name: Dara Adib
    Login: akhilsun             Name: Akhil Sundararajan
    Login: mdarabi              Name: ZARA MARISA DARABIFARD
    Login: eeden                Name: Elana Dara Eden
