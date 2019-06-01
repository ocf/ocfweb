[[!meta title="approve: record an OCF group account request"]]

This page explains the OCF account approval procedure and the usage of the
`approve` script.

## When to use approve

OCF group accounts need to be manually approved by staff in the lab. All
members requesting individual accounts should be directed to the online
approval page. If a member requesting an individual account cannot use the
online approval system (likely because of an invalid/unacceptable CalNet UID),
direct them to an OCF officer.

## Approving a request

**The approve program can only be run from supernova.**

### Before approve

* SSH into supernova.ocf.berkeley.edu

* For registered student groups, the OCF requires that a signatory authorize
  the approval of the account. If the account is not a registered student
  group, check with the [[membership eligibility|doc membership/eligibility]]
  to see what constitutes acceptable documentation.

* If the group is a registered student group, you can look up the requester's
  signatory status by name with [[signat|doc staff/howto/account-management/signat]].

  ```text
  $ signat name matthew mcallister
  Searching for people... Found 1 entry.
  Searching for signatories...

  MATTHEW JAMES Mcallister (1031366)
  ==================================
  Group                    Accounts                       OID
  -----------------------  ---------------------------  -----
  Open Computing Facility  decal, linux, ggroup, group  46187
  ```

  Copy the group's OID, as you will need it when running approve.

* If the group is not a student group, the requester will need an official
  letterhead giving them authority to create the account. You will also need to
  check that the group doesn't already have an account using
  `checkacct`.

  ```text
  $ checkacct privacy
  Login: bipla              Name: Berkeley Information Privacy Law Association
  ```

* Finally, check that the name on the requester's Cal ID matches who
  they say they are.


### Running approve

When you run approve it will open a text editor; just fill out the form,
save it, and let the requester enter a password when prompted.

For reference, `user_name` will be the username used to log in to the
newly-created account, `group_name` is the full name of the group, e.g.
'Open Computing Facility', and `email` should ideally point somewhere that
will be read by whoever will be maintaining the account. `signatory` has been
deprecated.

Optionally, if you pass the OID as the only argument, the `group_name`,
`callink_oid`, and `email` fields will get filled in automatically using the
group's public information on CalLink. If the group is not a student group,
(e.g. a research group), use 0 as the OID.


### Post approval

Explain to the requesters that they will need to apply for [[virtual
hosting|doc services/vhost]] after they have set up their site if they wish to
do so. Point them to relevant wiki articles.
