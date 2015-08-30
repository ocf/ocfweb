[[!meta title="signat: check signatory status"]]

## Introduction

Obtains a list of active student groups registered with the LEAD Center for which an OCF member or CalNet UID is a signatory.

For signatories without OCF accounts, you can lookup CalNet UIDs in the [CalNet directory](https://calnet.berkeley.edu/directory/). However, we still recommend that signatories [[request an individual account|doc membership]].

We require that a signatory be present (or authorize) any administrative tasks (account approval, password resets, and account enabling) for student groups registered with the LEAD Center.

## Technical notes

This Python script queries the [CalLink API](https://wikihub.berkeley.edu/pages/viewpage.action?pageId=80479487) with a CalNet UID and parses the returned XML as a Python dictionary which is in turn output as a YAML document. For OCF usernames, the CalNet UID is obtained from [[LDAP|doc staff/backend/ldap]].

## Usage

    $ signat
    Returns active student group information for a signatory.
    OCF username or CalNet UID is the first and only argument.

    Required packages: python-ldap, python-yaml

    $ signat daradib
    46187: Open Computing Facility
    91232: Zoroastrian Student Organization

    via
    https://apis.berkeley.edu/callink

If the Zoroastrian Student Organization was requesting a group account, the CalLink organization ID to use in [[approve|doc staff/scripts/approve]] would be 91232.

    $ signat 872544
    46187: Open Computing Facility
    91232: Zoroastrian Student Organization

    via
    https://apis.berkeley.edu/callink
