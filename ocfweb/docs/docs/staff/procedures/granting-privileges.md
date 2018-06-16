[[!meta title="Granting staff privileges"]]

## Adding people to groups

### `ocfstaff`

If you have root privileges, you can add or remove people from `ocfstaff` by
editing the group in LDAP:

```text
$ kinit you/admin
you/admin@OCF.BERKELEY.EDU's Password:
$ ldapvi '(cn=ocfstaff)'
```

Then add or remove the appropriate `memberUid` attribute.

### `ocfroot`

Before giving anyone root privileges, make sure to obtain authorization from
the SM.

Adding or removing people from `ocfroot` is similar to modifying
`ocfstaff`. However, if you are adding someone to root staff, in addition to
modifying LDAP, you will also have to create their `/root` and `/admin`
principals (if those don't already exist). For example, to create the
`/admin` principal, you would do:

```text
$ kadmin
kadmin> add otherstaffer/admin
you/admin@OCF.BERKELEY.EDU's Password:
Max ticket life [1 day]:
Max renewable life [1 week]:
Principal expiration time [never]:
Password expiration time [never]:
Attributes []:
Policy [default]:
otherstaffer/admin@OCF.BERKELEY.EDU's Password:
Verify password - otherstaffer/admin@OCF.BERKELEY.EDU's Password:
```

At the very first prompt, you are prompted for your password. It's safe to
accept the defaults for the next few prompts. The last two prompts should be
filled in by the new root staffer; it will become the password for their
`/root` or `/admin` principal.

After you've created these principals, you'll need to grant them powers in the
[Kerberos ACL file in Puppet](https://github.com/ocf/puppet/blob/master/modules/ocf_kerberos/files/kadmind.acl).

Also add the new root staffer to the Admin team in our GitHub org and grant
them RT admin privileges.


## Granting IRC chanop status

TODO


## Granting firewall access

In order to gain access to the firewall, it is necessary to email someone
from the ASUC Student Union to ask them to fill out the Telecom Shopping
Cart on your behalf. Send them an email with the CalNet IDs of the people
you want to add to the firewall, and have an existing firewall administrator
authorize the request. As of Fall 2017, the
[Facilities Coordinator](https://studentunion.berkeley.edu/our-team/) has
worked to get new people added to the firewall, although it is likely that
this process will change in Spring/Fall 2018 when the firewall is changed as
part of the [bSecure](https://bsecure.berkeley.edu) project.


## Giving people InCommon DCA access

We are able to obtain signed certificates at no charge through the campus
InCommon-Comodo certificate service. In order to gain access to this service, a
staffer needs to be listed as a Departmental Certificate Administrator for the
OCF. A current DCA can add other DCAs by sending a request to
[calnet-admin@berkeley.edu](mailto:calnet-admin@berkeley.edu).

 Refer to the service's [help
page](https://calnetweb.berkeley.edu/calnet-technologists/calnet-incommon-comodo-certificate-service)
for more information.
