[[!meta title="check: get details about an OCF user"]]

## Introduction

`check` allows staffers to get account details about users. Some information
may only be accessible to privileged users or root, or depend on the server
`check` is being run on, so output may differ accordingly.

`check` is best run on `supernova`.

`check` currently returns:

* `getent` (i.e. LDAP) info
* CalNet info
* Remaining print quota
* Virtual host, apphost, and/or virtual mail configuration if applicable
* DNS records for any of the above
* Signatory of / signatories for
* [[Notes|doc staff/howto/account-management/note]] about the user in `~staff/User_Info`
* Processes running on the current machine owned by that user
* Recent login history on the current machine by that user

## Usage/Example

    $ check sanjayk
    sanjayk:*:18298:20:Sanjay Krishnan:/home/s/sa/sanjayk:/bin/tcsh
    Member of group(s): ocf ocfstaff admin
    Mail forwarded to "|procmail #sanjayk"
    CalNet UID number: 646431
    CalNet affilations: AFFILIATE-TYPE-ADVCON-ALUMNUS AFFILIATE-TYPE-ADVCON-STUDENT EMPLOYEE-TYPE-ACADEMIC STUDENT-TYPE-REGISTERED

    Recent login history on local machine:
    -------------------------------------------------------------------------------
    pts/5 Fri Mar 8 10:42 - 10:58 (00:16) avalanche.ocf.berkeley.edu
    pts/17 Fri Mar 8 10:16 - 10:28 (00:11) avalanche.ocf.berkeley.edu
    pts/5 Wed Mar 6 18:14 - 19:54 (01:39) reccev-wism-wlan-189-130.airbears.berkeley.edu
    pts/5 Wed Mar 6 18:05 - 18:05 (00:00) reccev-wism-wlan-189-130.airbears.berkeley.edu
    pts/5 Mon Mar 4 19:04 - 19:05 (00:01) destruction.ocf.berkeley.edu
    -------------------------------------------------------------------------------
