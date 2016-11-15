[[!meta title="check: get details about an OCF user"]]

## Introduction

Check allows a staffer to get all the usage details of a user. Some information
may only be accessible to privileged users or root, and dependent on local
machine, so the output may differ accordingly.

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
