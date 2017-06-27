[[!meta title="check: get details about an OCF user"]]

## Introduction

`check` allows staffers to get account details about users. Some information
may only be accessible to privileged users or root, or depend on the local
machine, so the output may differ accordingly. `check` is best run on `supernova`.

`check` currently returns:

* `getent` info
* CalNet info
* Print Quota
* Virtual Host/Apphost info if group account
* Signatory for/signatories of
* [[Notes|doc staff/scripts/note]] about the user in `~staff/User_Info`
* Currently running processes on local machines
* Recent Logins

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
