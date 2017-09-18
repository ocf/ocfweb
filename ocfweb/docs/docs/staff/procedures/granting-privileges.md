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

Adding or removing people from `ocfroot` is similar. However, if you are adding
someone to root staff, in addition to modifying LDAP, you will also have to
create their `/root` and `/admin` principals (if those don't already exist):

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


## Granting IRC chanop status

TODO


## Granting firewall access

TODO


## Giving people InCommon DCA access

We are able to obtain signed certificates at no charge through the campus
InCommon-Comodo certificate service. In order to gain access to this service, a
staffer needs to be listed as a Departmental Certificate Administrator for the
OCF. Refer to the service's [help
page](https://calnetweb.berkeley.edu/calnet-technologists/calnet-incommon-comodo-certificate-service)
for information on how to do that.
