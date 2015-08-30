[[!meta title="approve: record an OCF account request"]]
This page explains the OCF account approval procedure and the usage of the ("approve") script.

## Using approve
OCF group accounts need to be manually approved by staff in the lab. All members requesting individual accounts should be directed to the online approval page. If a member requesting an individual account cannot use the online approval system (likely because of an invalid/unacceptable CalNet id), direct them to an OCF officer.

** The approve program may only be run from supernova.ocf.berkeley.edu **

## Before Approve
* SSH into supernova.ocf.berkeley.edu
* Check to see whether the group has an existing OCF account with [[checkacct|doc staff/scripts/checkacct]]. You should try different variants of the group's name as it may not have been correctly entered (eg. acronym etc.).

        $ checkacct Open
        Login: api                        Name: Open API Project
        Login: openu                      Name: Open University
        Login: oai                        Name: Open Access Initiative at Berkeley

* If the group does not have an account, ask the requester to fill out and sign a form (located near the staff computer).
* For registered student groups, the OCF requires that a signatory authorizes the approval of the account. If the account is not a registered student group check with the [[membership eligibility|doc membership/eligibility]] to see what constitutes acceptable documentation. If they are **not** a registered student group skip the next step.
* If the group is a registered student group, you can check the signatory status with the [[signat|doc staff/scripts/signat]]. There are three acceptable cases: (1) Student is a signatory and has an OCF account (2) Student is a signatory but does not have an OCF account (3) the student is not a signatory and has a note from a signatory.
* Case 1:

        $signat sanjayk
        46187: Open Computing Facility

* Case 2. Lookup the student's Calnet UID with the [Berkeley Directory](http://directory.berkeley.edu). Then run signat with the CalnetUID.

        $signat 646431
        46187: Open Computing Facility

* Case 3: Lookup the signatory in the note with the [Berkeley Directory](http://directory.berkeley.edu). Then run signat with **their** CalnetUID.

        $signat 872544
        46187: Open Computing Facility

* Note the number corresponding to the appropriate group (eg. 46187 Open Computing Facility) and confirm the student's identity from their CAL ID.

## Run Approve
When you run approve it will open a text editor to enter the following information:

    $ approve
    account_name: ocf
    callink_oid: 46187
    email: gm@ocf.berkeley.edu
    forward: true
    group_name: Open Computing Facility
    responsible: Dara Adib

    # Please ensure that:
    #  * Person requesting account is signatory of group (see signat)
    #  * Group does not have existing account (see checkacct)
    #  * Requested account name is based on group name
    #  * Paper form is signed
    #
    # To get the CalLink organization ID, use signat

    Enter password:
    Enter password again:
    Account request recorded

### Post approval

Explain that the account will be created in approximately one week and that they will need to apply for [[virtual hosting|doc services/vhost]] (if desirable) after they have set up their site. Point them to relevant wiki articles.
